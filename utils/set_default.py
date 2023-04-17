from telebot import TeleBot
from telebot.types import BotCommand
from config.conf import COMMANDS


def set_default_commands(bot: TeleBot):
    commands = [
        BotCommand(command=command[0], description=command[1])
        for command in COMMANDS
    ]
    bot.set_my_commands(commands)