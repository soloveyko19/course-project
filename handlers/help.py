"""
Module instead for bot command "/help"
"""

from telebot.types import Message
from loader import bot
from config.conf import COMMANDS


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:
    """
    Message handler which catch the command "/help"
    Print a list of abilities of this bot

    Args:
        message (Message): user's message
    """
    text = "Команди які знає цей бот:\n"
    for command in COMMANDS:
        text += "/" + command[0] + " - " + command[1] + "\n"
    bot.send_message(message.chat.id, text)
