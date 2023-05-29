"""
Module instead to bot command "/cancel"
"""

from loader import bot
from telebot.types import Message, CallbackQuery


@bot.message_handler(commands=["cancel"])
def cancel_all_states(message: Message):
    """
    Message handler for the command "/cancel"
    Delete oll the states and return a user to main menu

    Args:
        message (Message): user's message
    """
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Всі стани користувача скинуто.\n"
        "Ви повернулися до головного меню.\n"
        "Довідка по командам: /help",
    )


@bot.callback_query_handler(func=lambda data: data.data == "cancel")
def callback_cancel(callback: CallbackQuery):
    """
    Callback handler which catching a callback with "cancel" data
    Delete oll the states and return a user to main menu

    Args:
        callback: User's callback from keyboard
    """
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.send_message(
        callback.message.chat.id,
        "Всі стани користувача скинуто.\n"
        "Ви повернулися до головного меню.\n"
        "Довідка по командам: /help",
    )
