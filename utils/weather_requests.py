"""
The module intended for sending a http requests to weather API
"""

import requests
import json
from config.conf import RAPIDAPI_KEY
from datetime import datetime as dt


headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "weather338.p.rapidapi.com",
}


def get_cities(city_name: str):
    """
    Function to get a dict of cities where key is name and value is keys at API

    Args:
        city_name (str): name of city to search

    Returns: Dict of cities where key is name of city and key is key of city at API
    """
    querystring = {"query": city_name, "language": "uk-UA"}
    url = "https://weather338.p.rapidapi.com/locations/search"

    response = requests.get(url=url, params=querystring, headers=headers, timeout=100)
    if response.status_code == 200:
        cities = dict()
        all_info = dict(json.loads(response.text))
        if all_info.get("location"):
            for number, location in enumerate(all_info["location"]["address"]):
                cities[location] = all_info["location"]["placeId"][number]
                if number == 4:
                    break
            return cities


def get_city_detail(city_id):
    """
    Function to get city detail like as latitude longitude and correct name of city

    Args:
        city_id: key of city in API

    Returns: dict which contains latitude? longitude and name of the city
    """
    url = "https://weather338.p.rapidapi.com/locations/get-details"
    querystring = {"placeid": city_id, "language": "uk-UA"}
    response = requests.get(headers=headers, params=querystring, url=url, timeout=100)
    if response.status_code == 200:
        info = json.loads(response.text)
        city = dict()
        city["latitude"] = info["location"]["latitude"]
        city["longitude"] = info["location"]["longitude"]
        city["city_name"] = info["location"]["city"]
        return city


def get_weather_hourly(latitude, longitude):
    """
    Function to get weather hourly

    Args:
        latitude: latitude of selected city
        longitude: longitude of selected city

    Returns: dict with info about weather hourly
    """
    url = "https://weather338.p.rapidapi.com/weather/forecast"
    querystring = {
        "date": dt.now().strftime("%Y%m%d"),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m",
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=100)
    if response.status_code == 200:
        info = dict(json.loads(response.text))
        info = info.get("v3-wx-forecast-hourly-10day")
        return info


def get_today_weather(latitude, longitude):
    """
    Function to get weather today

    Args:
        latitude: latitude of selected city
        longitude: longitude of selected city

    Returns: dict with info about weather for today
    """
    url = "https://weather338.p.rapidapi.com/weather/forecast"
    querystring = {
        "date": dt.now().strftime("%Y%m%d"),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m",
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=100)
    if response.status_code == 200:
        info = dict(json.loads(response.text))
        info = info.get("v3-wx-observations-current")
        return info


def get_10_days_weather(latitude, longitude):
    """
    Function to get weather today

    Args:
        latitude: latitude of selected city
        longitude: longitude of selected city

    Returns: dict with info about weather for 10 days
    """
    url = "https://weather338.p.rapidapi.com/weather/forecast"
    querystring = {
        "date": dt.now().strftime("%Y%m%d"),
        "latitude": latitude,
        "longitude": longitude,
        "language": "uk-UA",
        "units": "m",
    }
    response = requests.get(url=url, params=querystring, headers=headers, timeout=100)
    if response.status_code == 200:
        info = dict(json.loads(response.text))
        info = info["v3-wx-forecast-daily-15day"]["daypart"][0]
        return info
