# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Heweather.py
 
@Time    :   2020-01-03 17:58
 
@Desc    :
 
'''

import requests
import re

KEY = "&key=9dc30f9838b64439805c40d26d727255"
CITY = "location=hefei"
# APIURL = "https://free-api.heweather.com/s6/"
APIURL = "https://free-api.heweather.net/s6/weather/"
USERNAME = "Acring"

s = requests.session()

class HeWeather(object):
    now_text = ""
    now_raw = []
    city_text = ""
    city_raw = []

    def __init__(self):
        self.city()

    # 利用获取IP地址的网页，获取本地城市名
    # @staticmethod
    # def getcity():
    #     inf = s.get("http://ip.lockview.cn/ShowIP.aspx").text
    #     cityname = re.findall(r"省(.*?)市", inf)[0]
    #     return cityname

    # 实况天气
    def now(self, cityname):
        api_type = "now?"
        # url = https://free-api.heweather.com/v5/now?city=深圳&key=2d849c62d67a4b9e94607d0f1c744561
        # url = APIURL + KEY + CITY
        cityname = 'location=' + cityname
        # apitype = "daily_forecast?"
        apitype = "now?"
        url = APIURL + apitype + cityname + KEY
        raw_json = s.get(url).json()
        if raw_json["HeWeather6"][0]["status"] != "ok":
            return
        self.now_raw = raw_json
        now_basic = raw_json["HeWeather6"][0]["basic"]        # 城市相关信息
        now_now = raw_json["HeWeather6"][0]["now"]            # 返回天气相关信息
        basic_city = now_basic["location"]  # 城市
        now_tmp = now_now["tmp"]  # 实时气温
        now_cond = now_now["cond_txt"]  # 天气描述
        now_fl = now_now["fl"]  # 体感温度
        now_dir = now_now["wind_dir"]  # 风向
        now_sc = now_now["wind_sc"]  # 风力
        now_spd = now_now["wind_spd"]  # 风速(kmph)

        text = """
                实时天气:
                亲爱的 {},您所在的地区为 {} ,
                现在的天气是 {}天,
                气温为 {}°
                体感气温为 {}°
                风向 {},
                风速 {}
                """.format(USERNAME, basic_city, now_cond, now_tmp, now_fl, now_dir, now_spd)
        self.now_text = text
        return text

    def city(self):
        # cityname = self.getcity()
        cityname = 'location=beijing'
        apitype = "now?"
        # url = https://free-api.heweather.com/v5/search?city=host&key=2d849c62d67a4b9e94607d0f1c744561
        url = APIURL + apitype + cityname + KEY

        raw_json = s.get(url).json()
        if raw_json["HeWeather6"][0]["status"] != "ok":
            return "获取天气失败:", raw_json["HeWeather5"][0]["status"]

        basic = raw_json["HeWeather6"][0]["basic"]
        self.city_raw = basic
        basic_city = basic["location"]
        basic_cnty = basic["cnty"]
        basic_id = basic["cid"]
        basic_prov = basic["parent_city"]  # 所属省会

        city = "&city=" + basic_city

        global CITY
        CITY = city
        city = "国家:{} 城市:{} 所属省会:{} 城市代码:{}".format(basic_cnty, basic_city, basic_prov, basic_id)
        self.city_text = city
        return


if __name__ == '__main__':
    heWeather = HeWeather()
    now = heWeather.now(cityname='hefei')
    print(now)