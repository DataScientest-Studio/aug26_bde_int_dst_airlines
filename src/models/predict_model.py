from pathlib import Path
import joblib
import pandas as pd


class HoldingPredictor:

    def __init__(self, model_path: Path = Path("models/holding_model.joblib")):
        model = joblib.load(model_path)
        self.preprocessor = model["preprocessor"]
        self.model = model["model"]

    def predict(
        self,
        airport_icao: str,
        main: str,
        temperature_c: float,
        wind_speed_mps: float,
        wind_direction_deg: float,
        wind_gust_mps: float = 0.0,
        cloudiness_percent: float = 0.0,
        visibility_m: float = 10000.0,
    ) -> dict:
        df = pd.DataFrame(
            [
                {
                    "airport_icao": airport_icao,
                    "main": main,
                    "temperature_c": temperature_c,
                    "wind_speed_mps": wind_speed_mps,
                    "wind_direction_deg": wind_direction_deg,
                    "wind_gust_mps": wind_gust_mps,
                    "cloudiness_percent": cloudiness_percent,
                    "visibility_m": visibility_m,
                }
            ]
        )

        X_encoded = self.preprocessor.transform(df)
        prediction = bool(self.model.predict(X_encoded)[0])
        proba = float(self.model.predict_proba(X_encoded)[0][1])

        return {
            "is_holding_predicted": prediction,
            "holding_probability": round(proba, 4),
        }