# Smart-Trip-ETA

## Live Demo

[Click here to try the live app](https://smart-trip-eta.onrender.com)

A machine learning project that predicts taxi trip duration based on travel distance, pickup time, day of the week, month, and passenger count.

## Project Overview

Smart-Trip-ETA was developed to understand how different factors affect taxi travel time and to build a model capable of estimating trip duration before a ride begins.

The project started with exploratory data analysis on a real-world taxi trip dataset, followed by data cleaning, feature engineering, visualization, model building, and deployment through a Flask web application.

## Problem Statement

Estimating travel time is useful for both passengers and transportation services. Trip duration can vary depending on distance, time of day, day of the week, and other factors.

The goal of this project is to analyze historical taxi trip data and predict the expected travel duration using machine learning techniques.

## Dataset

The dataset contains taxi trip records with information such as:

* Pickup and drop locations
* Distance traveled
* Pickup time
* Passenger count
* Trip duration

## Work Done

### Data Preprocessing

* Removed outliers from trip duration
* Handled unnecessary records
* Created useful features from date and time information

### Exploratory Data Analysis

* Trip duration distribution
* Hour-wise trip analysis
* Weekend vs weekday analysis
* Correlation analysis
* Feature importance analysis

### Machine Learning Models

The following models were trained and evaluated:

* Linear Regression
* Random Forest Regression

Random Forest produced the best results and was selected as the final model.

### Model Performance

* Mean Absolute Error (MAE): ~226 seconds
* R² Score: ~0.71

## Web Application

A Flask-based web application was developed to allow users to:

* Enter trip details
* Predict trip duration
* View previous predictions
* Store prediction history using SQLite

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Flask
* SQLite
* HTML
* CSS

## Project Structure

* charts/ → Visualizations generated during analysis
* notebook/ → Data analysis and machine learning notebook
* webapp/ → Flask application, templates, static files, and trained model
* README.md → Project documentation
* requirements.txt → Required Python libraries

## Future Improvements

* Deploy the application online
* Add interactive dashboards
* Use larger datasets
* Improve prediction accuracy with advanced models


