import os
from contextlib import closing

import psycopg2

from common.airports import load_airports

'''
Insertion of the airports from airports.json into public.airport table.
First, check the timezone: insert into public.timezone if not yet present. 
Next, insert new airport into public.airport if not exists.
'''

def main():
    airports = load_airports()
    inserted_airports = 0

    with closing(psycopg2.connect(database=os.environ["AIRLINES_DB_NAME"],
                                  host=os.environ["AIRLINES_DB_HOST"],
                                  user=os.environ["AIRLINES_DB_USER"],
                                  password=os.environ["AIRLINES_DB_PASSWORD"],
                                  port=os.environ["AIRLINES_DB_PORT"]
                                  )) as conn:
        with conn:
            with conn.cursor() as cur:
                for airport_icao, airport in airports.items():
                    cur.execute(
                        """
                        insert into public.timezone (name)
                        values (%s)
                        on conflict (name) do nothing
                        """,
                        (airport["timezone"],)
                    )

                    cur.execute(
                        """
                        select timezone_id
                        from public.timezone
                        where name = %s
                        """,
                        (airport["timezone"],)
                    )
                    timezone_id = cur.fetchone()[0]

                    bbox = airport["opensky_bbox"]

                    cur.execute(
                        """
                        insert into public.airport (
                            airport_icao, name, iata, city,
                            latitude, longitude, timezone,
                            lamin, lamax, lomin, lomax
                        )
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        on conflict (airport_icao) do nothing
                        """,
                        (
                            airport_icao, airport["name"], airport["iata"], airport["city"],
                            airport["latitude"], airport["longitude"], timezone_id,
                            bbox["lamin"], bbox["lamax"], bbox["lomin"], bbox["lomax"]
                        )
                    )

                    inserted_airports += cur.rowcount

    print(
        f"Airport ingestion complete: "
        f"{inserted_airports} new, "
        f"{len(airports) - inserted_airports} already present."
    )

if __name__ == "__main__":
    main()
