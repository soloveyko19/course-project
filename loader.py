"""
Module which loads all dependent modules
"""

from telebot import TeleBot
from config.conf import BOT_TOKEN
from utils.set_default import set_default_commands
from telebot import custom_filters

bot = TeleBot(token=BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))
set_default_commands(bot)
