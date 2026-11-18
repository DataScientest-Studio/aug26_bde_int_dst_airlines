from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.databases.dependencies.get_database import get_db
from pypika import Query, Table, Order, functions as fn, Parameter, Field

class Get_Flight_Summary:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_flight_summary", self.get_flight_summary, methods=["GET"])

    def get_flight_summary(self, date=None, db: Database = Depends(get_db)):

        if not date:
            date = str(date.today()) if 'date' in globals() else str(__import__('datetime').date.today())

        air_rows = self.get_aircraft_in_the_air(db, date)
        flight_rows = self.get_count_flights(db, date)
        airport_rows = self.get_busiest_airport(db)

        aircraft_in_the_air = air_rows[0]['count_in_air'] if air_rows else 0
        flights_today = flight_rows[0]['count'] if flight_rows else 0
        busiest_airport = airport_rows[0]['iata'] if airport_rows else 'N/A'

        return {
            'flights_today': flights_today,
            'aircraft_in_the_air': aircraft_in_the_air,
            'busiest_airport': busiest_airport
        }
        
    def get_aircraft_in_the_air(self, db: Database, date=None):

        # SQL:
        # select count(*) as count_on_ground 
        # from flight_state 
        # where on_ground = false
        flight_state = Table('flight_state')

        query = (
            Query.from_(flight_state)
            .select(fn.Count(flight_state.aircraft_icao24).distinct().as_('count_in_air'))
            .where(flight_state.on_ground == False)
            .where(fn.Date(flight_state.created_at) == Parameter('%s'))
        )

        result = db.execute_sql(query.get_sql(), (date,))

        return result
    
    def get_count_flights(self, db: Database, date):
        flight_state = Table('flight_state')

        query = (
            Query.from_(flight_state)
            .select(fn.Count(flight_state.aircraft_icao24).distinct().as_('count'))
            .where(fn.Date(flight_state.created_at) == Parameter('%s'))
        )

        result = db.execute_sql(query.get_sql(), (date,))

        return result

    def get_busiest_airport(self, db: Database):
        # SQL:
        # SELECT a.iata 
        # FROM flight_state fs 
        # JOIN airport a 
        # ON fs.airport_icao = a.airport_icao 
        # GROUP BY a.iata 
        # ORDER BY count(*) DESC 
        # LIMIT 1'

        fs = Table('flight_state').as_('fs')
        a = Table('airport').as_('a')

        query = (
            Query.from_(fs)
            .join(a)
            .on(fs.airport_icao == a.airport_icao)
            .select(a.iata)
            .groupby(a.iata)
            .orderby(fn.Count('*'), order=Order.desc)
            .limit(1)
        )
        
        sql_string = query.get_sql()
        result = db.execute_sql(sql_string)

        return result