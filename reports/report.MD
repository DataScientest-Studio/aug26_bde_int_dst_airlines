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


src/data/flightstats_api.py:
 - a script which calls the flightstats api and edit the data

src/databases:
 - a folder about all databases that we using

src/databases/database.py:
 - the database connection and functions about the CRUD-Systems

src/utils: 
 - Contains general helper modules and utility functions.
 
src/utils/api.py:
 - model and error handling about the api, that we don't need this in every script

src/utils/env_loader.py:
 - A utility function to load and validate environment variables from the .env file.

reports/database_documentation.md:
  - Documentation of the PostgreSQL database schema, including table structures, fields, data types, and API mappings for OpenSkyAPI and OpenWeatherAPI.

reports/figures/er_diagram.png:
  - The visual Entity-Relationship

## API evaluation and source selection

The original concept required both live aircraft positions and scheduled-flight data.
Several APIs were evaluated before selecting the sources used in the current
pipeline.

### Air France--KLM Open Data

A Flight Status API key was issued, but requests to the documented endpoint,
including its required time-range parameters, returned HTTP 404 responses from
the operational-flight route. The versioned route produced the same result. A
support ticket was submitted but received no response. Air France--KLM data are
therefore not used by the implemented pipeline.

### Other evaluated APIs

- **Lufthansa API:** deprecated and therefore unavailable for a new project.
- **FlightStats:** access was requested, but the supplied credentials provided
  Cirium Sky access instead.
- **Cirium Sky:** the available access covered only a 14-day data window and
  could not support the intended ongoing collection of live airport traffic.

### Aviationstack

Aviationstack was evaluated as a source of arrivals, departures, airline, and
schedule data. A live-flight request returned 100 records per response and
reported several thousand matching records, so complete retrieval requires
pagination. The tested plan does not permit date filtering or historical
requests: those requests returned `function_access_restricted`.

The free plan is also limited to 100 requests per month. Even a minimal design
that polls arrivals and departures for two airports daily would require about
120 requests per month, before processing additional pages. It therefore cannot
provide complete or timely schedule data for this project. The related database
entities (`travel`, `airline`, and `status`) remain in the schema for possible
future use with a suitable data source, but no Aviationstack collector or
normaliser is currently active.

### Selected sources

- **OpenSky** is the primary source of live aircraft state vectors. It supplies
  aircraft identifiers, position, altitude, velocity, direction, ground status,
  and observation timestamps inside an airport-specific bounding box.
- **OpenWeather** supplies current weather observations for each airport's
  configured latitude and longitude.

The project consequently focuses on observed air traffic around airports,
rather than on a complete timetable or a commercial flight-tracking service.
