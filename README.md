# Data Science Master's thesis - Earthquake Prediction

## 0. INTRODUCTION

Due to my period living in Chile, I am afraid of earthquakes and I think that analyzing the data collected about these phenomena can help me in this regard.

With this work I don't try to predict future earthquakes, I know that it's not possible. My intention is to know them a little bit better and practice some of the models learned during my Master of Data Science.

This work is divided in 3 parts:

1. Data Processing and Understanding,

2. Time Series (ARIMA and LSTM) 

3. Supervised learning models (Classification and regression)

## 1. Data Processing and Understanding

si hubiera tiempo scrapping https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=1979-01-01%2000:00:00&endtime=2019-06-08%2023:59:59&maxlatitude=-17.979&minlatitude=-57.136&maxlongitude=-64.863&minlongitude=-80.332&minmagnitude=2.5&orderby=time

### 1.1. DataFrame used

:clipboard: **original_data**
Data downloaded from https://earthquake.usgs.gov/earthquakes/search/ in csv format.
Columns used from csv: `id, time, latitude, longitude, depth, mag and place.`
Columns related to station where data were collect are discarded.

:clipboard: **sismos** = original_data plus the following calculated columns:
* `date, hour, year and month`
* `YM`(=[year]-[month])
* `magtype` = {__low__: mag in [0,4), __medium__: mag in [4,6), __high__: mag in [6,10)}
* `city`= nearest city to hypocenter get from column place
* `distcity` = distance from hypocenter to nearest city get from column place

:clipboard: **frequency_year** = number of seisms and maximun magnitude per year and magtype

:clipboard: **mag_ym** = maximun magnitude per month/year. Months without data are all from before 1991, I assume there were worst stations than now and not all seisms were collected. So I fill missing data with the average of maximum per month/year.

## 1.2. Conclusions

:chart_with_upwards_trend: The greater magnitude, the less depth

![alt text](./images/Conclusion1.png)

:chart_with_upwards_trend: Previous a big earthquake, the number of medium earthquake increases drastically

![alt text](./images/Conclusion2.png)

## 2. Time Series 

### 2.1. ARIMA 

### 2.2. LSTM

## 3. Supervised Learning Models 

### 3.1. Classification 

### 3.2. Regression
