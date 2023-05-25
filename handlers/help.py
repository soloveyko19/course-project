from telebot.types import Message
from loader import bot
from config.conf import COMMANDS


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:
    text = "Команди які знає цей бот:\n"
    for command in COMMANDS:
        text += "/" + command[0] + " - " + command[1] + "\n"
    bot.send_message(message.chat.id, text)
