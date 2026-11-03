from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.databases.dependencies.get_database import get_db

class Get_Flight_Summary:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_flight_summary", self.get_flight_summary, methods=["GET"])

    def get_flight_summary(self, date, db: Database = Depends(get_db)):

        air_rows = self.get_aircraft_in_the_air(db)
        flight_rows = self.get_count_flights(db, date)
        airport_rows = self.get_busiest_airport(db)

        aircraft_in_the_air = air_rows[0]['count_on_ground'] if air_rows else 0
        flights_today = flight_rows[0]['count'] if flight_rows else 0
        busiest_airport = airport_rows[0]['iata'] if airport_rows else 'N/A'

        return {
            'flights_today': flights_today,
            'aircraft_in_the_air': aircraft_in_the_air,
            'busiest_airport': busiest_airport
        }
        
    def get_aircraft_in_the_air(self, db: Database):
        query = 'select count(*) as count_on_ground from flight_state where on_ground = false'
        result = db.execute_sql(query)

        return result
    
    def get_count_flights(self, db: Database, date):
        if date: 
            query = 'SELECT count(*) FROM flight_state WHERE DATE(created_at) = %s'
            result = db.execute_sql(query, (date,))
        else: 
            query = 'SELECT count(*) FROM flight_state WHERE DATE(created_at) = CURRENT_DATE'
            result = db.execute_sql(query)

        return result

    def get_busiest_airport(self, db: Database):
        query = 'SELECT a.iata FROM flight_state fs JOIN airport a ON fs.airport_icao = a.airport_icao GROUP BY a.iata ORDER BY count(*) DESC LIMIT 1'
        result = db.execute_sql(query)

        return result