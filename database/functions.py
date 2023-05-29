"""
Module than contain functions to work with database
"""

from .models import UserInfo


def new_user(user_id):
    """
    Function which checks if user already has in database

    Args:
        user_id: user's telegram id

    Returns: True if user was created, False if user already has in database
    """
    user, created = UserInfo.get_or_create(user_id=user_id)
    return created


def get_user_city(user_id):
    """
    Function that returned info about user's city from database
    Args:
        user_id: user's telegram id

    Returns: dict with info about city if it contains in database

    """
    info = UserInfo.get(UserInfo.user_id == user_id)
    if info.city_id:
        city_info = {
            "id": info.city_id,
            "latitude": info.latitude,
            "longitude": info.longitude,
            "city_name": info.city_name,
        }
        return city_info


def set_user_city(user_id, city_id, city_name, latitude, longitude):
    """
    Function to set the details about selected city in the database

    Args:
        user_id: user's telegram id
        city_id: id of selected city in API
        city_name: name of selected city
        latitude: latitude of selected city
        longitude: longitude of selected city
    """
    info = UserInfo.get(UserInfo.user_id == user_id)
    info.city_name = city_name
    info.city_id = city_id
    info.longitude = longitude
    info.latitude = latitude
    info.save()
