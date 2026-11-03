class AirportModel:
    def __init__(self, icao, latitude, longitude, timezone, lamin, lamax, lomin, lomax, iata = None, city = None):
        self.icao = icao
        self.iata = iata
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.lamin = lamin
        self.lomin = lomin
        self.lamax = lamax
        self.lomax = lomax