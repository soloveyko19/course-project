"""
Module instead for bot command "/weather"
"""

from telebot.types import Message, CallbackQuery
from loader import bot
from database.functions import get_user_city
from .city import change_city
from utils import weather_requests
from keyboards.inline import inline_keyboad_by_dict
from datetime import datetime as dt


@bot.message_handler(commands=["weather"])
def weather_start(message: Message) -> None:
    """
    Message handler which catching the command "/weather".
    Send a keyboard with choice of view a weather

    Args:
        message (Message): user's message
    """
    city_info = get_user_city(message.chat.id)
    if city_info:
        keyboard = inline_keyboad_by_dict(
            {
                "Погода сьогодні": "today",
                "Наступні 24 години (погодинно)": "hourly",
                "10 днів": "10 days",
            }
        )
        bot.send_message(
            message.chat.id, "Як саме хочете переглядати погоду?", reply_markup=keyboard
        )
    else:
        change_city(message)


@bot.callback_query_handler(func=lambda data: data.data in ("today", "hourly", "10 days"))
def get_weather(callback: CallbackQuery):
    """
    Function which catching callback from keyboard of choice the view a weather and returned a message with weather
    which user selected earlier.

    Args:
        callback (CallbackQuery): callback from inline keyboard
    """
    msg = bot.send_message(callback.message.chat.id, "Одну секунду, дізнаюсь погоду...")
    city = get_user_city(callback.from_user.id)

    if callback.data == "hourly":
        weather = weather_requests.get_weather_hourly(
            city.get("latitude"), city.get("longitude")
        )
        bot.delete_message(msg.chat.id, msg.id)
        if weather:
            text = ""
            text_template = (
                "{smile} {time} ({day})\n"
                "🌡 Температура: {temp}°С, відчувається як {temp_like}°С\n"
                "💦 Вологість повітря: {humidity}%\n"
                "🔆 УФ-індекс: {uv_index} з 10 ({uv_description})\n"
                "Опади: {precip_type} {precip_chance}% {precip_quantity}мм\n\n"
            )

            for hour in range(24):
                precip = weather.get("precipType")[hour]

                text += text_template.format(
                    smile="☀️" if weather.get("dayOrNight")[hour] == "D" else "🌙",
                    time=dt.fromisoformat(weather.get("validTimeLocal")[hour][:-5]).strftime("%H:%M"),
                    day=weather.get("dayOfWeek")[hour],
                    temp=weather.get("temperature")[hour],
                    temp_like=weather.get("temperatureFeelsLike")[hour],
                    humidity=weather.get("relativeHumidity")[hour],
                    uv_index=weather.get("uvIndex")[hour],
                    uv_description=weather.get("uvDescription")[hour],
                    precip_type="Дощ 💧" if precip == "rain" else "Сніг ❄️",
                    precip_chance=weather.get("precipChance")[hour],
                    precip_quantity=weather.get("qpf")[hour] if precip == "rain" else weather.get("qpfSnow")[hour]
                )
        else:
            text = "Сталася непередбачувана помилка 😳"
        bot.send_message(callback.message.chat.id, text)

    elif callback.data == "today":
        weather = weather_requests.get_today_weather(
            city.get("latitude"), city.get("longitude")
        )
        bot.delete_message(msg.chat.id, msg.id)
        if weather:
            text = (
                "{day_part} Погода сьогодні ({day}) в {city_name}\n\n"
                "{description}\n\n"
                "⬇️ Тиск: {pressure} мбар\n\n"
                "🌡 Температура зараз: {temp}°С, відчувається як {temp_like}°С\n\n"
                "🌡 Мінімальна: {temp_min}°С, максимальна {temp_max}°С\n\n"
                "💦 Вологість повітря: {humidity}%\n\n"
                "🔆 УФ-індекс: {uv_index} з 10\n\n"
                "👀 Видимість: {visibility}\n\n"
                "💧 Точка роси: {dew_point}°С"
            ).format(
                day_part="☀️" if weather.get("dayOrNight") == "D" else "🌙",
                day=weather.get("dayOfWeek"),
                city_name=city.get("city_name"),
                description=weather.get("wxPhraseLong"),
                pressure=weather.get("pressureMeanSeaLevel"),
                temp=weather.get("temperature"),
                temp_like=weather.get("temperatureFeelsLike"),
                temp_min=weather.get("temperatureMin24Hour"),
                temp_max=weather.get("temperatureMax24Hour"),
                humidity=weather.get("relativeHumidity"),
                uv_index=weather.get("uvIndex"),
                visibility=weather.get("visibility"),
                dew_point=weather.get("temperatureDewPoint")
            )
        else:
            text = "Сталася непередбачувана помилка 😳"

        bot.send_message(callback.message.chat.id, text)

    elif callback.data == "10 days":
        weather = weather_requests.get_10_days_weather(
            city.get("latitude"), city.get("longitude")
        )
        bot.delete_message(msg.chat.id, msg.id)
        if weather:
            text_template = (
                "{smile} {daypart_name}\n"
                "🌡 Температура: {temp}°С\n"
                "☁️ Хмарність: {clouds}%\n"
                "🔆 УФ-індекс: {uv_index} з 10\n"
                "Опади: {precip_type} {precip_chance}% {precip_quantity}мм\n"
                "{description}\n\n"
            )

            for day in range(0, 20, 2):
                text = ""
                night = day + 1

                if weather.get("dayOrNight")[day]:
                    precip = weather.get("precipType")[day]
                    text += text_template.format(
                        daypart_name=weather.get("daypartName")[day],
                        smile="☀️",
                        temp=weather.get("temperature")[day],
                        clouds=weather.get("cloudCover")[day],
                        uv_index=weather.get("uvIndex")[day],
                        precip_chance=weather.get("precipChance")[day],
                        precip_type="Дощ 💧" if precip == "rain" else "Сніг ❄️",
                        precip_quantity=weather.get("qpf")[day] if precip == 'rain'
                        else weather.get("qpfSnow")[day],
                        description=weather.get("wxPhraseLong")[day]
                    )

                if weather.get("dayOrNight")[night]:
                    precip = weather.get("precipType")[night]
                    text += text_template.format(
                        daypart_name=weather.get("daypartName")[night],
                        smile="🌙",
                        temp=weather.get("temperature")[night],
                        clouds=weather.get("cloudCover")[night],
                        uv_index=weather.get("uvIndex")[night],
                        precip_chance=weather.get("precipChance")[night],
                        precip_type="Дощ 💧" if weather.get("precipType")[night] == "rain" else "Сніг ❄️",
                        precip_quantity=weather.get("qpf")[night] if precip == 'rain'
                        else weather.get("qpfSnow")[night],
                        description=weather.get("wxPhraseLong")[night],
                    )
                bot.send_message(callback.message.chat.id, text)
        else:
            bot.send_message(callback.message.chat.id, "Сталася непередбачувана помилка 😳")
    weather_start(callback.message)
