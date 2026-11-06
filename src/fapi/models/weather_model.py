class WeatherModel:
    def __init__(self, weather_states_id, temp, wind_speed, wind_deg, cloudiness_persent, time_of_record, main, description, icon_id):
        self.weather_states_id = weather_states_id
        self.temp = temp
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.cloudiness_persent = cloudiness_persent
        self.time_of_record = time_of_record
        self.main = main
        self.description = description
        self.icon_id = icon_id