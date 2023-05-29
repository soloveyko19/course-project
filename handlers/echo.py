"""
Module instead for messages than don't match any other condition
"""

from loader import bot
from telebot.types import Message


@bot.message_handler(state=None)
def echo(message: Message) -> None:
    """
    Message handler which catching the other messages that don't match any other condition

    Args:
        message (Message): user's message
    """
    bot.send_message(
        message.chat.id,
        "Я не розумію що ви маєте на увазі.\n" f'Ваше повідомлення "{message.text}".',
    )
