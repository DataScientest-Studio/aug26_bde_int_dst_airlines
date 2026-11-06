class FlightModel:
    def __init__(self, flight_state_id, callsign, time_position, last_contact, longitude, latitude, baro_altitude, on_ground, velocity, true_track, velocity_rate, geo_altitude):
        self.flight_state_id = flight_state_id
        self.callsign = callsign
        self.time_position = time_position
        self.last_contact = last_contact
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track
        self.velocity_rate = velocity_rate
        self.geo_altitude = geo_altitude