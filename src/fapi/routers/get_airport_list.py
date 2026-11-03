from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.airport_model import AirportModel
from src.databases.dependencies.get_database import get_db


class Get_Airport_List:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_airport_list", self.get_airport_list, methods=["GET"])

    def get_airport_list(self, db: Database = Depends(get_db)):
        rows = self.get_airport_rows(db)
        max_count = self.get_airport_max_count(db)

        airport_list = []

        for r in rows:
            airport = AirportModel(
                icao = r["airport_icao"], 
                iata = r["iata"],
                city = r["city"],
                latitude = r["latitude"],
                longitude = r["longitude"],
                timezone = r["timezone"],
                lamin = r["lamin"],
                lamax = r["lamax"],
                lomin = r["lomin"],
                lomax = r["lomax"]
            )
            airport_list.append(airport)
        

        return {
            "airport_list": airport_list,
            "max_count": max_count
        }

    def get_airport_rows(self, db: Database):
        query = 'select * from airport'
        result = db.execute_sql(query)

        return result

    def get_airport_max_count(self, db: Database):
        query = 'select count(*) from airport'
        result = db.execute_sql(query)

        return result