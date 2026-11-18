class WeatherModel:
    def __init__(self, weather_states_id, temp, wind_speed, wind_direction_deg, wind_gust_mps, cloudiness_percent, time_of_record, main, description, icon_id):
        self.weather_states_id = weather_states_id
        self.temp = temp
        self.wind_speed = wind_speed
        self.wind_direction_deg = wind_direction_deg
        self.wind_gust_mps = wind_gust_mps
        self.cloudiness_percent = cloudiness_percent
        self.time_of_record = time_of_record
        self.main = main
        self.description = description
        self.icon_id = icon_id