"""
Module to set default settings for bot
"""

from telebot import TeleBot
from telebot.types import BotCommand
from config.conf import COMMANDS


def set_default_commands(bot: TeleBot):
    """
    Function to set default commands

    Args:
        bot (TeleBot): your bot
    """
    commands = [
        BotCommand(command=command[0], description=command[1]) for command in COMMANDS
    ]
    bot.set_my_commands(commands)
