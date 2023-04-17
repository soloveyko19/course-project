from .models import UserInfo


def new_user(user_id):
    user, created = UserInfo.get_or_create(user_id=user_id)
    return created


def get_user_city(user_id):
    info = UserInfo.get(UserInfo.user_id == user_id)
    if info.city_id:
        city_info = {
            'id': info.city_id,
            'latitude': info.latitude,
            'longitude': info.longitude,
            'city_name': info.city_name
        }
        return city_info
    else:
        return None


def set_user_city(user_id, city_id, city_name, latitude, longitude):
    info = UserInfo.get(UserInfo.user_id == user_id)
    info.city_name = city_name
    info.city_id = city_id
    info.longitude = longitude
    info.latitude = latitude
    info.save()

