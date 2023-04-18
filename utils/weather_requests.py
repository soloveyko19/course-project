import requests
import json
from config.conf import RAPIDAPI_KEY
from datetime import datetime as dt


headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "weather338.p.rapidapi.com"
}


def get_cities(city_name: str):
    querystring = {
        'query': city_name,
        'language': 'uk-UA'
    }
    url = "https://weather338.p.rapidapi.com/locations/search"

    response = requests.get(url=url, params=querystring, headers=headers, timeout=5)
    if response.status_code == 200:
        cities = dict()
        all_info = dict(json.loads(response.text))
        for number, location in enumerate(all_info['location']['address']):
            cities[location] = all_info['location']['placeId'][number]
            if number == 4:
                break
        return cities
    else:
        return None


def get_city_detail(city_id):
    url = 'https://weather338.p.rapidapi.com/locations/get-details'
    querystring = {
        "placeid": city_id,
        "language": "uk-UA"
    }
    response = requests.get(headers=headers, params=querystring, url=url, timeout=5)
    if response.status_code == 200:
        info = json.loads(response.text)
        city = dict()
        city['latitude'] = info['location']['latitude']
        city['longitude'] = info['location']['longitude']
        city['city_name'] = info['location']['city']
        return city
    else:
        return None


def get_weather_hourly(latitude, longitude):
    url = 'https://weather338.p.rapidapi.com/weather/forecast'
    querystring = {
        "date": dt.now().strftime('%Y%m%d'),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m"
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=5)
    if response.status_code == 200:
        all_info = json.loads(response.text)
        my_info = list()
        for i in range(24):
            new_info = dict()
            new_info['time'] = dt.fromisoformat(all_info['vt1runweatherhourly']['fcstValidLocal'][i][:-5])
            new_info['d_or_n'] = all_info['vt1runweatherhourly']['dayInd'][i]
            new_info['temperature'] = int(((int(all_info['vt1runweatherhourly']['temperature'][i]) - 32) * (5 / 9)))
            new_info['rain_prob'] = all_info['vt1runweatherhourly']['precipPct'][i]
            new_info['cloud_cover'] = all_info['vt1runweatherhourly']['cloudPct'][i]
            new_info['wind_speed'] = all_info['vt1runweatherhourly']['windSpeed'][i]
            my_info.append(new_info)
        return my_info


def get_today_weather(latitude, longitude):
    url = 'https://weather338.p.rapidapi.com/weather/forecast'
    querystring = {
        "date": dt.now().strftime('%Y%m%d'),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m"
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=5)
    if response.status_code == 200:
        info = json.loads(response.text)
        weather = dict()
        weather['city'] = info['v3-location-point']['location']['city'] + \
                          ', ' + \
                          info['v3-location-point']['location']['adminDistrict'] + \
                          ', ' + \
                          info['v3-location-point']['location']['country']
        weather['weather'] = info['v3-wx-observations-current']['cloudCoverPhrase']
        weather['temp_day'] = info['v3-wx-observations-current']['temperatureMax24Hour']
        weather['temp_night'] = info['v3-wx-observations-current']['temperatureMin24Hour']
        weather['temp'] = info['v3-wx-observations-current']['temperature']
        weather['temp_like'] = info['v3-wx-observations-current']['temperatureFeelsLike']
        weather['wind_speed'] = info['v3-wx-observations-current']['windSpeed']
        weather['request_time'] = dt.fromisoformat(info['v3-wx-observations-current']['validTimeLocal'][:-5])
        weather['sunrise'] = dt.fromisoformat(info['v3-wx-observations-current']['sunriseTimeLocal'][:-5])
        weather['sunset'] = dt.fromisoformat(info['v3-wx-observations-current']['sunsetTimeLocal'][:-5])
        weather['pressure'] = info['v3-wx-observations-current']['pressureAltimeter']
        return weather
    else:
        return None


def get_10_days_weather(latitude, longitude):
    url = 'https://weather338.p.rapidapi.com/weather/forecast'
    querystring = {
        "date": dt.now().strftime('%Y%m%d'),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m"
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=5)
    if response.status_code == 200:
        info = json.loads(response.text)
        weather = list()
        for i in range(10):
            new_day = dict()
            new_day['day_of_week'] = info['v3-wx-forecast-daily-15day']['dayOfWeek'][i]
            new_day['temp_max'] = info['v3-wx-forecast-daily-15day']['temperatureMax'][i]
            new_day['temp_min'] = info['v3-wx-forecast-daily-15day']['temperatureMin'][i]
            new_day['moon_phase'] = info['v3-wx-forecast-daily-15day']['moonPhase'][i]
            new_day['sunrise'] = dt.fromisoformat(info['v3-wx-forecast-daily-15day']['sunriseTimeLocal'][i][:-5])
            new_day['sunset'] = dt.fromisoformat(info['v3-wx-forecast-daily-15day']['sunsetTimeLocal'][i][:-5])
            weather.append(new_day)
        return weather

