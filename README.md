# Weather_Data_Analysis

## Project Overview
The purpose of this project is to analyze the past weather data for a given location within a given range of dates-of-the-year (e.g. London, UK averaged 5 rainy days between March 25 and April 3 in the past 17 years) to predict the weather of that location. The interactive dashboard presents analysis of the weather data, including temperature, wind speed, rain, snowfall, and humidity, etc. So a front-end user could access our website and utilize the tool to retrieve instant and informative weather information about a given location for trip planning. 

## Motivation & Questions to Answer
### Motivation
Weather is an interesting and data-rich subject that naturally lends itself to this course. We have already seen how .json files packed with interesting data can be obtained freely from api calls made available from sites like openweather and deployed in visually compelling styles with google maps. 

More broadly, however, who doesn’t think weather is interesting? Weather is everywhere, all the time. It is among the most common conversational topics worldwide. Weather influences our daily activities, our travel destination choices, even our emotional state. Weather is dramatic, violent, occasionally very dangerous and, more now than perhaps at any other time in human history, of critical importance to the planet.

Thinking more specifically about travel destination choices or trip planning with respect to weather, our project will attempt to create a tool that provides a front-end user with weather information for a destination that they specify based on historical weather data obtained from our API call. This feature should be interesting for not only members of our class but for the general public. A hypothetical front-end user from the public should theoretically be able to access and utilize our tool to retrieve real, informative weather information about a given location. Such a tool has real value.

### Questions to Answer
This project will try to answer at least some of the following questions:

* Is it still feasible to replicate or approximate the old Trip Planner feature from Weather Underground? Trip Planner was an interactive, user-inputted function that returned weather-related information to a front-end user based on certain criteria that was of interest. One of our questions is to determine whether this type of feature can be recreated or approximated.

* Can a machine learning model adequately categorize and cluster, and then return to a front-end user correct or generally realistic weather conditions for a specific season and/or location? A key question of this project is to determine whether a machine-learning tool can return accurate/realistic weather-related information to a user based on location and (perhaps) time of year inputs the user provides. A sensitive and precise machine learning program returning weather-related predictions would be very interesting and potentially very powerful.

## Data Sets/ Data Tools Used
* Data Source: [Data Source](https://open-meteo.com/en/docs/historical-weather-api)
* Language: 
    * Python, Flask, Machine Learning
        * Dependecies: pandas, numpy, scipy,  matplotlib, scikit-learn
    * JavaScript, HTML, CSS
        * Libraries: Bootstrap, D3, plotly
* Software: Jupyter Notebook, VSCode

