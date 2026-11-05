from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.airport_model import AirportModel
from src.databases.dependencies.get_database import get_db
from pypika import Query, Table, functions as fn

class Get_Airport_List:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_airport_list", self.get_airport_list, methods=["GET"])

    def get_airport_list(self, db: Database = Depends(get_db)):
        rows = self.get_airport_rows(db)
        raw_count = self.get_airport_max_count(db)

        max_count = raw_count[0]["count"] if raw_count else 0

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
        # SQL:
        # select * from airport
        
        airport_table = Table('airport')
        query = Query.from_(airport_table).select('*')
        sql_string = query.get_sql()

        result = db.execute_sql(sql_string)

        return result

    def get_airport_max_count(self, db: Database):
        # SQL:
        # select count(*) from airport
        airport_table = Table('airport')
        query = Query.from_(airport_table).select(fn.Count('*').as_('count'))
        sql_string = query.get_sql()

        result = db.execute_sql(sql_string)

        return result