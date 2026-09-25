# Project Airlines
==============================

This project is an MLOps pipeline designed for processing flight data and model predictions.
------------
## Getting Started

Follow these steps to set up the development environment on your local machine.

### Prerequisites
1. Make sure you have **Python 3.10+** and **pip** installed on your system.
2. Create a virtual environment (.venv):
    - python3 -m venv .venv
3. Activate the virtual environment: 
    - On macOS / Linux (WSL): source .venv/bin/activate
    - On Windows (PowerShell): .venv\Scripts\Activate.ps1
4. Install required dependencies: 
    - pip install -r requirements.txt
5. copy env.template and rename it into .env and add credentials

------------

## Project Organization


    ├── env.template       <- Template to initialize config data. Copy this file, rename it to .env, and add your config data. 
    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                          generated with `pip freeze > requirements.txt`
    │
    ├── main.py            <- main script to execute the code
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data         
    │   │   ├── api.py     <- general API function
    │   │   └── flightstats_api.py <- get Flightstats data by Flightstats-API
    │   │
    │   ├── databases       <- Database config
    │   │   └──  database.py <- functions to get/store/delete data from the database 
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── utils          <- Contains general helper modules and utility functions.
    │   │   └── env_loader.py <- load variables from .env file
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
