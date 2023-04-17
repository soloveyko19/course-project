from telebot.types import Message, CallbackQuery
from loader import bot
from database.functions import get_user_city
from .city import change_city
from utils import weather_requests
from keyboards.inline import inline_keyboad_by_dict


@bot.message_handler(commands=['weather'])
def weather_start(message: Message):
    city_info = get_user_city(message.chat.id)
    if city_info:
        keyboard = inline_keyboad_by_dict(
            {
                'Погода сьогодні': 'today',
                'Почасово': 'hourly',
                '10 днів': '10 days',
            }
        )
        bot.send_message(
            message.chat.id,
            'Як саме хочете переглядати погоду?',
            reply_markup=keyboard
        )
    else:
        change_city(message)


@bot.callback_query_handler(func=lambda data: data.data in ('today', 'hourly', '10 days'))
def get_weather(callback: CallbackQuery):
    msg = bot.send_message(callback.message.chat.id,
                           'Одну секунду, дізнаюсь погоду...')

    city = get_user_city(callback.from_user.id)
    if callback.data == 'hourly':
        weather = weather_requests.get_weather_hourly(city.get('latitude'), city.get('longitude'))
        bot.delete_message(msg.chat.id, msg.id)
        text = ''
        day = weather[0]['time']
        for hour in weather:
            if hour['time'].day != day.day:
                text += hour['time'].strftime('%d.%m.%Y\n\n')
                day = hour['time']
            text += '{smile} {time} {temp}°C\n💧{rain}% {clouds}%☁️ \nВітер - {wind}км/г🌬\n\n'.format(
                smile='🌙' if hour['d_or_n'] == 'N' else '☀️',
                time=hour['time'].strftime('%H:00'),
                temp=hour['temperature'],
                rain=hour['rain_prob'],
                clouds=hour['cloud_cover'],
                wind=hour['wind_speed'],
            )
        bot.send_message(callback.message.chat.id, text)
    elif callback.data == 'today':
        weather = weather_requests.get_today_weather(city.get('latitude'), city.get('longitude'))
        bot.delete_message(msg.chat.id, msg.id)
        text = f'Погода сьогодні у {weather.get("city")}\n' \
               f'{weather.get("request_time").strftime("%H:%M")}\n\n' \
               f'{weather.get("weather")}\n\n' \
               f'Температура зараз: {weather.get("temp")}°С\n' \
               f'Відчувається як: {weather.get("temp_like")}°С\n\n' \
               f'Максимальна температура вдень: {weather.get("temp_day")}°С\n' \
               f'Мінімальна температура вночі: {weather.get("temp_night")}°С\n' \
               f'Щвидкість вітру: {weather.get("wind_speed")} км/г\n' \
               f'Світанок: {weather.get("sunrise").strftime("%H:%M")}\n' \
               f'Захід сонця: {weather.get("sunset").strftime("%H:%M")}\n' \
               f'Атмосферний тиск: {weather.get("pressure")} мм рт. ст.'
        bot.send_message(callback.message.chat.id, text)
    elif callback.data == '10 days':
        weather = weather_requests.get_10_days_weather(city.get('latitude'), city.get('longitude'))
        bot.delete_message(msg.chat.id, msg.id)
        text = ''
        for day in weather:
            text += f'{day["day_of_week"]}\n' \
                    f'Максимальна температура: {day["temp_max"]}°С\n' \
                    f'Мінімальна температура: {day["temp_min"]}°С\n' \
                    f'Фаза місяця: {day["moon_phase"]}\n' \
                    f'Погода: {day["narrative"]}\n\n'
        bot.send_message(callback.message.chat.id, text)
    weather_start(callback.message)




