from loader import bot
from telebot.types import Message, CallbackQuery
from states.states import CityStatesStorage
from utils import weather_requests
from keyboards.inline import inline_keyboad_by_dict
from database.functions import set_user_city


@bot.message_handler(commands=['city'], state=None)
def change_city(message: Message) -> None:
    bot.set_state(
        user_id=message.chat.id,
        state=CityStatesStorage.city_name,
        chat_id=message.chat.id
    )
    bot.send_message(message.chat.id, 'Добре, введіть місто для відстежування.')


@bot.message_handler(state=CityStatesStorage.city_name)
def confirm_city(message: Message) -> None:
    city = message.text.capitalize()
    message_ = bot.send_message(message.chat.id, f'Шукаю міста з назвою {city!r}...')
    cities = weather_requests.get_cities(city)
    bot.delete_message(message_.chat.id, message_.id)
    if cities:
        keyboard = inline_keyboad_by_dict(cities, back=True)
        bot.send_message(message.chat.id,
                         'Уточніть будь ласка',
                         reply_markup=keyboard)
    else:
        bot.send_message(
            message.chat.id,
            'Не вдалося знайти міста з такою назвою.\n'
            'Ви повернулися до головного меню')


@bot.callback_query_handler(func=lambda data: True, state=CityStatesStorage.city_name)
def get_city_id(callback: CallbackQuery):
    info = weather_requests.get_city_detail(callback.data)
    set_user_city(
        user_id=callback.from_user.id,
        city_id=callback.data,
        latitude=info.get('latitude'),
        longitude=info.get('longitude'),
        city_name=info.get('city_name')
    )
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, f'Занотовано, ваше місто {info["city_name"]!r}\n'
                                               f'Ви повернулися до головного меню')

