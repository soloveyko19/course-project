from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboad_by_dict(dct: dict, back: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for key, value in dct.items():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
    if back:
        keyboard.add((InlineKeyboardButton(text='Повернутися до головного меню 🔙', callback_data='cancel')))
    return keyboard
