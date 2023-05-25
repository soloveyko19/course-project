from telebot.handler_backends import StatesGroup, State


class CityStatesStorage(StatesGroup):
    city_name = State()
