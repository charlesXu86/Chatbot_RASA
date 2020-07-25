import datetime
import os

import requests

from service.weather_api.base import WeatherAPIBase
from service.weather_api.condition import Condition


class SeniverseWeatherAPI(WeatherAPIBase):
    DEFAULT_KEY = os.getenv('SENIVERSE_KEY', '')  # API key

    API_URL = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
    UNIT = 'c'  # 单位
    LANGUAGE = 'zh-Hans'  # 查询结果的返回语言

    def __init__(self, api_secret=None):
        self.key = api_secret if api_secret else self.DEFAULT_KEY

        super(SeniverseWeatherAPI, self).__init__()

    def _fetch_weather(self, location, start=0, days=15):
        result = requests.get(self.API_URL, params={
            'key': self.key,
            'location': location,
            'language': self.LANGUAGE,
            'unit': self.UNIT,
            'start': start,
            'days': days
        }, timeout=2)
        return result.json()

    def get_weather_by_city(self, city, *args, **kwargs):
        forecasts = self._fetch_weather(city)
        return self._forecasts_to_condition(forecasts)

    @staticmethod
    def _forecasts_to_condition(forecasts):
        condition_data = {}
        city = forecasts['results'][0]['location']['name']
        for i in forecasts['results'][0]['daily']:
            date = datetime.datetime.strptime(i['date'], '%Y-%m-%d').date()
            condition = Condition(date, i['text_day'], i['low'], i['high'])
            condition_data[date] = condition

        # condition = Condition(city, city)


        return condition_data

    def forecast_to_text(self, condition):
        msg_tpl = "{date} 的天气情况为：{condition}；气温：{temp_low}-{temp_high} 度"
        msg = msg_tpl.format(
            # city= condition.city,
            date=condition.date,
            condition=condition.condition,
            temp_low=condition.low_temperature,
            temp_high=condition.high_temperature
        )
        return msg


if __name__ == "__main__":
    api_secret = "Sq6NfAburbGs9MGQb"
    sw = SeniverseWeatherAPI(api_secret)
    data = datetime.datetime.strptime('2020-7-23', '%Y-%m-%d').date()
    ss = datetime.datetime.now().date()
    print(ss)
    result = sw.get_text_by_city_and_day('上海', ss)
    print(result)
