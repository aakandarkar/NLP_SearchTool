# SearchTool.py Documentation

**Author:** [Your Name]
**Last Updated:** [Date]

This document provides an overview of the `searchtool.py` script, which is a Python application for searching and matching offers using natural language processing techniques and cosine similarity.

## Table of Contents
1. [Introduction](#introduction)
    - [Purpose of the Script](#purpose-of-the-script)
    - [Dependencies](#dependencies)

2. [Usage](#usage)
    - [Running the Script](#running-the-script)
    - [User Interface](#user-interface)

3. [Functions](#functions)
    - [`map_retailer(offer_text)`](#map_retaileroffer_text)
    - [`get_matching_string(str1, str2)`](#get_matching_stringstr1-str2)
    - [`vectorize_data_based_on_metadata(product_input)`](#vectorize_data_based_on_metadataproduct_input)
    - [`index()`](#index)
    - [`search_offers()`](#search_offers)

4. [Data Sources](#data-sources)
    - [Brand Data](#brand-data)
    - [Category Data](#category-data)
    - [Offers Data](#offers-data)

5. [Setup and Execution](#setup-and-execution)
    - [Flask App Initialization](#flask-app-initialization)
    - [Routes and Endpoints](#routes-and-endpoints)

6. [Running the Application](#running-the-application)
    - [Starting the Application](#starting-the-application)
    - [Accessing the User Interface](#accessing-the-user-interface)

---

## 1. Introduction

### Purpose of the Script
The `searchtool.py` script is designed to match and search offers based on user queries. It uses natural language processing techniques, including text vectorization and cosine similarity, to identify relevant offers. The script also handles partial matching of retailer names to improve matching accuracy.

### Dependencies
The script utilizes various Python libraries and modules for its functionality, including `numpy`, `pandas`, `spacy`, `gensim`, `operator`, `re`, `fuzzywuzzy`, `sklearn`, and `flask`.

---

## 2. Usage

### Running the Script
To use the search tool, execute the script `searchtool.py`. The script initializes a Flask web application that allows users to search for offers and retrieve matching results.

### User Interface
The web interface allows users to input their search queries and submit them for processing. The results will be displayed in a tabular format, showing offers along with their similarity scores.

---

## 3. Functions

### `map_retailer(offer_text)`
Maps the retailer based on the presence of retailer keywords in the offer text. Returns the mapped retailer or "Unknown" if no match is found.

### `get_matching_string(str1, str2)`
Calculates the similarity score between two strings using the fuzzy string matching algorithm. Returns the second string if the similarity score is above a specified threshold; otherwise, returns "Unknown".

### `vectorize_data_based_on_metadata(product_input)`
Performs text vectorization using CountVectorizer on the metadata of products. Computes cosine similarity between the input query and all products. Returns a DataFrame of similar offers and their similarity scores.

### `index()`
Flask route function for the home page ("/"). Renders the main index.html template.

### `search_offers()`
Flask route function for the search page ("/search"). Handles POST requests containing user queries. Displays the search results in an HTML table.

---

## 4. Data Sources

The script uses three main data sources:
- **Brand Data**: A CSV file containing brand information, including brand names and associated product categories.
- **Category Data**: A CSV file with category data, including parent-child relationships between categories.
- **Offers Data**: A CSV file containing offer details, including the offer text and retailer information.

---

## 5. Setup and Execution

### Flask App Initialization
The script initializes a Flask web application named `app`.

### Routes and Endpoints
- The root route ("/") renders the index.html template, displaying the main search interface.
- The "/search" route handles user queries submitted via a POST request and displays the search results.

---

## 6. Running the Application

### Starting the Application
Run the script using the command `python searchtool.py`. This will start the Flask web application.

### Accessing the User Interface
Open a web browser and navigate to `http://localhost:3001` to access the search tool's user interface. Enter your search query and submit it to retrieve matching offers.

---
