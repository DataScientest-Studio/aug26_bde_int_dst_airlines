from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.flight_model import FlightModel
from src.fapi.models.weather_model import WeatherModel
from src.fapi.models.airport_model import AirportModel
from src.databases.dependencies.get_database import get_db


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
                latitude = row["airport_latitude"],
                longitude = row["airport_longitude"],
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

    def filter(self, date, time_from, time_to, iata, callsign):
        conditions = []
        params = []

        if date:
            conditions.append("DATE(TIMEZONE('Europe/Berlin', fs.last_contact)) = %s")
            params.append(date)

        if time_from:
            fmt = 'HH24:MI:SS' if len(time_from.strip()) > 5 else 'HH24:MI'
            conditions.append(f"TO_CHAR(TIMEZONE('Europe/Berlin', fs.last_contact), '{fmt}') >= %s")
            params.append(time_from.strip())

        if time_to:
            fmt = 'HH24:MI:SS' if len(time_to.strip()) > 5 else 'HH24:MI'
            conditions.append(f"TO_CHAR(TIMEZONE('Europe/Berlin', fs.last_contact), '{fmt}') <= %s")
            params.append(time_to.strip())

        if iata:
            conditions.append("a.iata = %s")
            params.append(iata.strip().upper())

        if callsign:
            conditions.append("fs.callsign ILIKE %s")
            params.append(f"%{callsign.strip()}%")

        where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        return where_sql, params
        
    def get_flight_rows(self, db: Database, limit, offset, date, time_from, time_to, iata, callsign):
        where_sql, params = self.filter(date, time_from, time_to, iata, callsign)
        params.extend([limit, offset])

        query = f"""
        with subselect as (
            select
            fs.*,
            a.iata,
            a.city,
            a.latitude as airport_latitude,
            a.longitude as airport_longitude,
            a.timezone,
            a.lamin,
            a.lomin,
            a.lamax,
            a.lomax,
            ws.weather_state_id,
            ws.temperature_c,
            ws.wind_speed_mps,
            ws.wind_direction_deg,
            ws.cloudiness_percent,
            ws.wind_gust_mps,
            ws.time_of_record,
            ws.weather_id,
            w.main,
            w.description,
            w.icon_id,
            row_number() over (
                partition by fs.flight_state_id
                order by
                    case
                        when (ws.time_of_record - fs.last_contact) < interval '0'
                        then -(ws.time_of_record - fs.last_contact)
                        else (ws.time_of_record - fs.last_contact)
                    end asc,
                ws.weather_state_id desc
            ) as rownumber
            from flight_state fs
            left join airport a
                on fs.airport_icao = a.airport_icao
            left join weather_state ws
                on a.airport_icao = ws.airport_icao
            left join weather w
                on ws.weather_id = w.weather_id
            {where_sql}
        )
        select *
        from subselect
        where rownumber = 1
        order by flight_state_id desc
        limit %s offset %s
        """

        return db.execute_sql(query, tuple(params))

    def get_flight_data_max_count(self, date, time_from, time_to, iata, callsign, db: Database):
        # SQL:
        # SELECT COUNT(*) 
        # FROM flight_state fs 
        # LEFT JOIN airport a ON fs.airport_icao = a.airport_icao 
        where_sql, params = self.filter(date, time_from, time_to, iata, callsign)

        query = f"""
        SELECT COUNT(*) AS count
        FROM flight_state fs
        LEFT JOIN airport a
            ON fs.airport_icao = a.airport_icao
        {where_sql}
        """

        result = db.execute_sql(query, tuple(params))

        return result