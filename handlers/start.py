"""
Module instead for bot command "/start"
"""

from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline import inline_keyboad_by_dict
from .weather import weather_start
from .city import change_city
from .help import help
from database.functions import new_user


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    """
    Message handler which catching the command "/start"
    If user is new, him get into database

    Args:
        message (Message): user's message
    """
    if new_user(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "Доброго дня, вельмешановне панство!\n" "Довідка по командам /help",
        )
    else:
        bot.send_message(message.chat.id, "Аутентифікацію пройдено")

    keyboard = inline_keyboad_by_dict(
        {
            "Подивитись погоду по місту": "weather",
            "Змінити місто відстежування": "change_city",
            "Вивести довідку по командам": "help",
        }
    )
    bot.send_message(
        message.chat.id, "Виберіть що хочете виконати", reply_markup=keyboard
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data in ("weather", "change_city", "help")
)
def start_callback(callback: CallbackQuery) -> None:
    """
    Callback handler which catching data with something what user want to do

    Args:
        callback (CallbackQuery): callback which user sent from keyboard
    """
    if callback.data == "weather":
        weather_start(message=callback.message)
    elif callback.data == "change_city":
        change_city(message=callback.message)
    elif callback.data == "help":
        help(message=callback.message)
