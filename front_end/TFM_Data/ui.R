library(shiny)
library(shinythemes)
library(dygraphs)
library(markdown)


# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Flatly Style
  theme = shinytheme("flatly"), # https://rstudio.github.io/shinythemes/
  
  navbarPage("Earthquake Analysis",
    tabPanel("Plots",
  
      # Sidebar with checkbox to filter by mangnitude
      sidebarLayout(
        sidebarPanel(
      
          checkboxGroupInput("checkMag", label = h5("Filter By Magnitude"), 
                             choices = list("2" = 2, "3" = 3, "4" = 4,  "5" = 5,  "6" = 6,  "7" = 7,  "8" = 8),
                             selected = c(2,3,4,5,6,7,8))

        ), # sidebarPanel
    
        # Show 2 graphics with max magitude and frequency per month/year
        mainPanel(
      
          dygraphOutput("plot_time_series", width = "100%", height = "200px"),
          dygraphOutput("plot_frequency", width = "100%", height = "200px")
          # conditionalPanel(condition = "input.radio_model == 'KN'",plotOutput("plot_lr")),
        
        ) # mainPanel
      ) # sidebarLayout
    ), # tabpanel plot
    tabPanel("Data",
        dataTableOutput('table')
             
    )
  ) # navbarPage
)) # Fluidpage
