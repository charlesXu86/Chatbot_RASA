class WeatherAPIBase(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_weather_by_city(self, city, *args, **kwargs):
        raise NotImplementedError

    def get_weather_by_city_and_day(self, city, date, *args, **kwargs):
        forecast_data = self.get_weather_by_city(city, *args, **kwargs)
        return forecast_data[date]

    def get_weather_by_location(self, lat, long, *args, **kwargs):
        raise NotImplementedError

    def forecast_to_text(self, forecast):
        raise NotImplementedError

    def get_weather_by_location_and_day(self, lat, long, date, *args, **kwargs):
        forecast_data = self.get_weather_by_location(lat, long, *args, **kwargs)
        return forecast_data[date]

    def get_text_by_city_and_day(self, city, date, *args, **kwargs):
        forecast_data = self.get_weather_by_city_and_day(city, date, *args, **kwargs)
        return self.forecast_to_text(forecast_data)
