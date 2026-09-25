# Project Airlines

1. Datastructure:
## original Project Structure: 

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
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

## new folders/files:
env.template:
 - A template for developers containing required environment variable keys without any sensitive data. Developers need to copy this file, rename it to .env, and insert their local credentials. This ensures consistent variable naming across the team without hardcoding secrets in the codebase.

main.py:
 - the main entry point of the application, eliminating the need to run individual scripts manually.

src/data/api.py:
 - model and error handling about the api, that we don't need this in every script

src/data/flightstats_api.py:
 - a script which calls the flightstats api and edit the data

src/databases:
 - a folder about all databases that we using

src/databases/database.py:
 - the database connection and functions about the CRUD-Systems

src/utils: 
 - Contains general helper modules and utility functions.

src/utils/env_loader.py:
 - A utility function to load and validate environment variables from the .env file.

## deleted folders/files: