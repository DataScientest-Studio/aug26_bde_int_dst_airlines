from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.flight_model import FlightModel
from src.fapi.models.weather_model import WeatherModel
from src.fapi.models.airport_model import AirportModel
from src.databases.dependencies.get_database import get_db
from pypika import PostgreSQLQuery, Query, Table, functions as fn, Parameter, CustomFunction, Order

ToChar = CustomFunction('TO_CHAR', ['column', 'fmt'])

class Get_Flight_List:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_flight_list", self.get_flight_list, methods=["GET"])

    def get_flight_list(self, limit=10, offset=0, date=None, time_from=None, time_to=None, iata=None, callsign=None, db: Database = Depends(get_db)):


        flight_data = self.get_flight_rows(db, limit, offset, date, time_from, time_to, iata, callsign)

        raw_count = self.get_flight_data_max_count(date, time_from, time_to, iata, callsign, db)
        max_count = raw_count[0]["count"] if raw_count else 0

        flight_list = []

        for row in flight_data: 

            flight = FlightModel(
                flight_state_id = row["flight_state_id"],
                callsign = row["callsign"],
                time_position = row["time_position"],
                last_contact = row["last_contact"],
                longitude = row["longitude"],
                latitude = row["latitude"],
                baro_altitude = row["baro_altitude"],
                on_ground = row["on_ground"],
                velocity = row["velocity"],
                true_track = row["true_track"],
                vertical_rate = row["vertical_rate"],
                geo_altitude = row["geo_altitude"]
            ) if row else {}

            weather = WeatherModel(
                weather_states_id = row["weather_state_id"],
                temp = row["temperature_c"],
                wind_speed = row["wind_speed_mps"],
                wind_direction_deg = row["wind_direction_deg"],
                cloudiness_percent = row["cloudiness_percent"],
                wind_gust_mps = row["wind_gust_mps"],
                time_of_record = row["time_of_record"],
                main = row["main"],
                description = row["description"],
                icon_id = row["icon_id"]
            )

            airport = AirportModel(
                icao = row["airport_icao"],
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
            'flight_list': flight_list,
            'max_count': max_count
        }

    def filter(self, query, fs, a, date, time_from, time_to, iata, callsign):

        params = []
        
        if date:
            query = query.where(fn.Date(fs.created_at) == Parameter('%s'))
            params.append(date)

        if time_from:
            fmt = 'HH24:MI:SS' if len(time_from.strip()) > 5 else 'HH24:MI'
            query = query.where(ToChar(fs.created_at, fmt) >= Parameter('%s'))
            params.append(time_from.strip())
 
        if time_to:
            fmt = 'HH24:MI:SS' if len(time_to.strip()) > 5 else 'HH24:MI'
            query = query.where(ToChar(fs.created_at, fmt) <= Parameter('%s'))
            params.append(time_to.strip())

        if iata:
            query = query.where(a.iata == Parameter('%s'))
            params.append(iata.upper())

        if callsign:
           query = query.where(fs.callsign.ilike(Parameter('%s')))
           params.append(f"%{callsign.strip()}%")
           
        return query, params
        
    def get_flight_rows(self, db: Database, limit, offset, date, time_from, time_to, iata, callsign):
        # SQL:
        # SELECT * 
        # FROM flight_state fs 
        # LEFT JOIN airport a ON fs.airport_icao = a.airport_icao 
        # LEFT JOIN weather_state ws ON a.airport_icao = ws.airport_icao
        
        fs = Table('flight_state').as_('fs')
        a = Table('airport').as_('a')
        ws = Table('weather_state').as_('ws')
        w = Table('weather').as_('w')

        query = (
            PostgreSQLQuery.from_(fs)
            .distinct_on(fs.flight_state_id)
            .select('*')
            .left_join(a)
            .on(fs.airport_icao == a.airport_icao)
            .left_join(ws)
            .on(a.airport_icao == ws.airport_icao)
            .left_join(w)
            .on(ws.weather_id == w.weather_id)
        )

        query, params = self.filter(query, fs, a, date, time_from, time_to, iata, callsign)
        query = query.limit(limit).offset(offset).orderby(fs.flight_state_id, order=Order.desc)

        result = db.execute_sql(query.get_sql(), tuple(params))

        return result

    def get_flight_data_max_count(self, date, time_from, time_to, iata, callsign, db: Database):
        # SQL:
        # SELECT COUNT(*) 
        # FROM flight_state fs 
        # LEFT JOIN airport a ON fs.airport_icao = a.airport_icao 
        fs = Table('flight_state')
        a = Table('airport')
        query = Query.from_(fs).select(fn.Count('*').as_('count')).left_join(a).on(fs.airport_icao == a.airport_icao)

        query, params = self.filter(query, fs, a, date, time_from, time_to, iata, callsign)

        result = db.execute_sql(query.get_sql(), tuple(params))

        return result