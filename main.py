from loader import bot
import handlers  # noqa
from utils.set_default import set_default_commands
from telebot import custom_filters


if __name__ == "__main__":
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling(skip_pending=True)
