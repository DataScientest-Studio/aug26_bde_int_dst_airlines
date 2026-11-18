import os
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

if not ENV_FILE.is_file():
    raise RuntimeError(f"Missing environment file: {ENV_FILE}")

class Database:
    def __init__(self):
        load_dotenv(ENV_FILE)
        self.dbconnection = self.create_db_connection()

    def create_db_connection(self):
        return psycopg2.connect(
            database=os.environ["AIRLINES_DB_NAME"],
            host=os.environ["AIRLINES_DB_HOST"],
            user=os.environ["AIRLINES_DB_USER"],
            password=os.environ["AIRLINES_DB_PASSWORD"],
            port=os.environ["AIRLINES_DB_PORT"]
        )

    def execute_sql(self, query, params=None):
        with self.dbconnection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)

            # if a query doesn't return anything (i.e. write-only), 
            # fetchall will make Pastgres to raise "no results to fetch"
            if cur.description is None:
                return []
            
            return cur.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.dbconnection.commit()
            else:
                self.dbconnection.rollback()
        finally:
            if self.dbconnection:
                self.dbconnection.close()
        return False # python doesn't hide the original exception
    