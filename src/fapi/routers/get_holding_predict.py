from fastapi import APIRouter

from src.models.predict_model import HoldingPredictor


class Get_Holding_Predict:

    def __init__(self):
        self.router = APIRouter()
        self.pred = HoldingPredictor()
        self.router.add_api_route("/get_holding_predict", self.predict_holding, methods=["GET"],)

    def predict_holding(
        self,
        airport_icao: str,
        main: str,
        temperature_c: float,
        wind_speed_mps: float,
        wind_direction_deg: float,
        wind_gust_mps: float = 0.0,
        cloudiness_percent: float = 0.0,
        visibility_m: float = 10000.0
    ) -> dict:
        return self.pred.predict(
            airport_icao=airport_icao,
            main=main,
            temperature_c=temperature_c,
            wind_speed_mps=wind_speed_mps,
            wind_direction_deg=wind_direction_deg,
            wind_gust_mps=wind_gust_mps,
            cloudiness_percent=cloudiness_percent,
            visibility_m=visibility_m
        )