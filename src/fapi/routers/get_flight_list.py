from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.flight_model import FlightModel
from src.fapi.models.weather_model import WeatherModel
from src.fapi.models.airport_model import AirportModel
from src.databases.dependencies.get_database import get_db
from pypika import Query, Table

class Get_Flight_List:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_flight_list", self.get_flight_list, methods=["GET"])

    def get_flight_list(self, db: Database = Depends(get_db)):


        flight_data = self.get_flight_rows(db)

        flight_list = []

        for row in flight_data: 

            flight = FlightModel(
                flight_states_id = row["flight_state_id"],
                callsign = row["callsign"],
                time_position = row["time_position"],
                last_contact = row["last_contact"],
                longitude = row["longitude"],
                latitude = row["latitude"],
                baro_altitude = row["baro_altitude"],
                on_ground = row["on_ground"],
                velocity = row["velocity"],
                true_track = row["true_track"],
                velocity_rate = row["velocity_rate"],
                geo_altitude = row["geo_altitude"]
            ) if row else {}

            weather = WeatherModel(
                weather_states_id = row["weather_state_id"],
                temp = row["temp"],
                wind_speed = row["wind_speed"],
                wind_deg = row["wind_deg"],
                cloudiness_persent = row["cloudiness_persent"],
                time_of_record = row["time_of_record"],
                main = row["main"],
                description = row["description"],
                icon_id = row["icon_id"]
            )

            airport = AirportModel(
                icao = row["icao"],
                iata = row["iata"],
                city = row["city"],
                latitude = row["latitude"],
                longitude = row["longitude"],
                timezone = row["timezone"],
                lamin = row["lamin"],
                lomin = row["lomin"],
                lamax = row["lamax"],
                lomax = row["lomax"]
            )

            flight_list.append({
                'flight': flight,
                'weather': weather,
                'airport': airport
            })

        return {
            'flight_list': flight_list
        }

    def get_flight_rows(self, db: Database):
        # SQL:
        # SELECT * 
        # FROM flight_state fs 
        # LEFT JOIN airport a ON fs.airport_icao = a.airport_icao 
        # LEFT JOIN weather_state ws ON a.airport_icao = ws.airport_icao
        
        fs = Table('flight_state').as_('fs')
        a = Table('airport').as_('a')
        ws = Table('weather_state').as_('ws')

        query = (
            Query.from_(fs)
            .select('*')
            .left_join(a)
            .on(fs.airport_icao == a.airport_icao)
            .left_join(ws)
            .on(a.airport_icao == ws.airport_icao)
        )

        sql_string = query.get_sql()

        result = db.execute_sql(sql_string)

        return result