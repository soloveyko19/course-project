"""
Main module for start a bot
"""

from loader import bot
import handlers  # noqa


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
