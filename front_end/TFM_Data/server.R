library(shiny)
library(shinyjs)
library(rpart)
library(rpart.plot)
library(dygraphs)
library(dplyr)
library(tidyverse)
library(htmlwidgets)
library(DT)


# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  # Read data
  sismos = read.csv('./../../data/earthquake.csv')
  
  # Create Columns
  sismos$'YM'<- as.Date(paste0(format(as.Date(sismos$time), "%Y-%m"), '-01'), format='%Y-%m-%d')
  sismos$'year'<- as.Date(paste0(format(as.Date(sismos$time), "%Y"), '-01-01'), format='%Y-%m-%d')
  sismos$'Date'<- format(as.Date(sismos$time), "%Y-%m-%d")
  sismos$'mag_int' <- as.integer(sismos[,'mag'])
  sismos$'mag_type' <- cut(sismos$mag,breaks = c(0, 4, 6, 10), labels = c("low", "medium", "high"))
  
  
  # Serie with all months from 1970 until Today
  allMonths <- seq.Date(as.Date("1970/01/01"),
                        max(as.Date(sismos$time)),
                        "month")
  
  # Serie with all years from 1970 until 2019
  allmonths_type <- merge(x=as.data.frame(seq.Date(as.Date("1970/01/01"), max(as.Date(sismos$time)),"month")), 
                         y= as.data.frame(c("low", "medium", "high")),
                         all.x = TRUE)
  cols <- c("YM","type")
  colnames(allmonths_type) <- cols
  
   # When Magnitude checkbox is clicked return sismos filtered and grouped by month/year
   sismos_filter <- reactive({
     
     ts <- merge(x=data.frame(allMonths),
                 y=sismos[sismos$mag_int %in% input$checkMag, c('YM','mag')] , 
                 by.x = c("allMonths"),
                 by.y = c("YM"),
                 all.x=TRUE) %>% 
           group_by(allMonths) %>% 
           summarise(mag = max(mag)) %>% 
           mutate(mag = if_else(is.na(mag), 0, mag))  # Fill NaN with 0
     ts(ts[,'mag'],frequency = 12, start = c(1970, 1))  # make it time serie
     
   })
   
   # Render Magnitude per month/year graph
  output$plot_time_series <- renderDygraph({
    dygraph(sismos_filter(), main = "Maximun Magnitude per Month/Year") %>%
      dySeries("mag", label = "Magnitude") %>%
      dyOptions(stackedGraph = TRUE) %>%
      dyRangeSelector(height = 20, dateWindow = c("2009-01-01", "2017-01-01"))
  })


  # When Magnitude checkbox is clicked return sismos filtered and grouped by month/year
  frequency_filter <- reactive({
    ts_type <- merge(x=allmonths_type,
                y=sismos[sismos$mag_int %in% input$checkMag, c('YM', 'mag_type','mag')] ,
                by.x = c("YM","type"),
                by.y = c("YM","mag_type"),
                all.x=TRUE)  %>%
      group_by(YM, type) %>%
      summarise_all(funs(freq = sum(!is.na(.)))) # Fill NaN with 0
    low <- ts(ts_type[ts_type$type=='low','freq'],frequency = 12, start = c(1970, 1))  # make it time serie
    medium <- ts(ts_type[ts_type$type=='medium','freq'],frequency = 12, start = c(1970, 1))  # make it time serie
    high <- ts(ts_type[ts_type$type=='high','freq'],frequency = 12, start = c(1970, 1))  # make it time serie
    cbind(low, medium, high)
    
  })

  # Render Magnitude per month/year graph
  output$plot_frequency <- renderDygraph({
    dygraph(frequency_filter(), main = "Frequency per Month/Year split by type") %>%
      dySeries("low", label = "Low [0,4)", color = "green") %>%
      dySeries("medium", label = "Medium [4, 6)", color = "orange") %>%
      dySeries("high", label = "High [6, )", color = "red") %>%
      dyLegend(width = 400)  %>%
      dyOptions(stackedGraph = TRUE) %>%
      dyRangeSelector(height = 20, dateWindow = c("2009-01-01", "2017-01-01")) %>%
      dyHighlight(highlightCircleSize = 5, 
                  highlightSeriesBackgroundAlpha = 0.2,
                  hideOnMouseOut = FALSE) %>%
      dyEvent("1985-3-1", "Valparaiso (Metropolitana) 8.0", labelLoc = "bottom") %>%
      dyEvent("1995-7-1", "Antofagasta (Norte) 8.0", labelLoc = "bottom") %>%
      dyEvent("2010-2-1", "Bio-Bio (Sur) 8.8", labelLoc = "bottom") %>%
      dyEvent("2014-4-1", "Iquique (Norte) 8.2", labelLoc = "bottom") %>%
      dyEvent("2015-9-1", "Illapel (Metropolitana) 8.3", labelLoc = "bottom")
  })
  
  # Table to show in Data Tab
  
  data_to_show <- sismos[,c('Date', 'mag_type', 'mag', 'depth', 'place')]
  
  output$table <- renderDataTable(
    datatable(data_to_show, 
              filter = 'top',
              options = list(
                        lengthMenu = list(c(5, 15, -1), c('5', '15', 'All')),
                        pageLength = 15)
    )
  )
  

})
