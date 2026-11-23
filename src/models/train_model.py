from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from src.databases.databases import Database

def load_training_data(db: Database) -> pd.DataFrame:
    sql_flights = """
    SELECT 
    fs.flight_state_id,
    fs.airport_icao,
    fs.aircraft_icao24,
    fs.time_position,
    fs.on_ground,
    fs.latitude,
    fs.longitude,
    fs.baro_altitude,
    fs.velocity,
    fs.vertical_rate,
    fs.true_track,
    a.latitude as airport_latitude,
    a.longitude as airport_longitude
    FROM flight_state fs
    LEFT JOIN airport a ON fs.airport_icao = a.airport_icao
    """
    
    flight_list = db.execute_sql(sql_flights)
    
    df_flights = pd.DataFrame(flight_list)

    # Weather data
    sql_weather = """
    SELECT 
    ws.weather_state_id,
    ws.airport_icao,
    ws.temperature_c,
    ws.wind_speed_mps,
    ws.wind_direction_deg,
    ws.wind_gust_mps,
    ws.cloudiness_percent,
    ws.visibility_m,
    ws.time_of_record,
    w.main,
    w.description
    FROM weather_state ws
    LEFT JOIN weather w ON ws.weather_id = w.weather_id
    """
    weather_list = db.execute_sql(sql_weather)

    df_weather = pd.DataFrame(weather_list)

    # clean flight data
    # only flights in the air
    df_flights = df_flights[df_flights['on_ground'] == False]

    # delete incomplete data points
    df_flights = df_flights.dropna(subset=['baro_altitude', 'velocity', 'vertical_rate'])

    # type object to type float
    df_flights['latitude'] = df_flights['latitude'].astype(float)
    df_flights['longitude'] = df_flights['longitude'].astype(float)
    df_flights['baro_altitude'] = df_flights['baro_altitude'].astype(float)
    df_flights['vertical_rate'] = df_flights['vertical_rate'].astype(float)
    df_flights['velocity'] = df_flights['velocity'].astype(float)
    df_flights['true_track'] = df_flights['true_track'].astype(float)
    df_flights['airport_latitude'] = df_flights['airport_latitude'].astype(float)
    df_flights['airport_longitude'] = df_flights['airport_longitude'].astype(float)

    # delete flights under 80 km/h (20 ms)
    df_flights = df_flights[df_flights['velocity'] > 20]

    # no steep climbs
    df_flights = df_flights[df_flights['vertical_rate'] <= 3.0]

    df_flights['is_holding'] = (
        ((df_flights['latitude'] - df_flights['airport_latitude']).abs() < 0.4) &
        ((df_flights['longitude'] - df_flights['airport_longitude']).abs() < 0.6) &
        (df_flights['baro_altitude'] < 3000) &
        (df_flights['velocity'] < 140) &
        (df_flights['vertical_rate'].between(-1.5, 1.5))
    )

    # clean weather data

    # fill wind_gust_map with 0
    df_weather['wind_gust_mps'] = df_weather['wind_gust_mps'].fillna(0)

    # delete incomplete data points 
    df_weather = df_weather.dropna(subset=['visibility_m'])

    # type object to type float
    df_weather['temperature_c'] = df_weather['temperature_c'].astype(float)
    df_weather['wind_speed_mps'] = df_weather['wind_speed_mps'].astype(float)
    df_weather['wind_gust_mps'] = df_weather['wind_gust_mps'].astype(float)

    # merge flight data with weather data
    df_flights = df_flights.sort_values('time_position').reset_index(drop=True)
    df_weather = df_weather.sort_values('time_of_record').reset_index(drop=True)

    df = pd.merge_asof(df_flights, df_weather, left_on='time_position', right_on='time_of_record', by='airport_icao')

    # delete Rows with no weather
    df = df.dropna(subset=['weather_state_id'])

    return df


def train_and_save_model(model_path: Path = Path("models/holding_model.joblib")) -> None:
    db = Database()
    df = load_training_data(db)

    X = df.drop(['is_holding', 'baro_altitude', 'velocity', 'vertical_rate', 'latitude', 'longitude', 'flight_state_id', 'aircraft_icao24', 'time_position', 'true_track', 'airport_latitude', 'airport_longitude',
        'weather_state_id', 'time_of_record', 'description', 'on_ground'], axis=1)
    y = df['is_holding']

    features = ['main', 'airport_icao']
    transformer = OneHotEncoder(drop='first', sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("data", transformer, features),
        ],
        remainder='passthrough'
    ).set_output(transform="pandas")

    X_encoded = preprocessor.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.20, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(random_state=42, class_weight="balanced")
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    print("Train score:", rf.score(X_train, y_train))
    print("Test score:", rf.score(X_test, y_test))
    print(classification_report(y_test, y_pred))

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "preprocessor": preprocessor,
            "model": rf,
        },
        model_path,
    )


if __name__ == "__main__":
    train_and_save_model()