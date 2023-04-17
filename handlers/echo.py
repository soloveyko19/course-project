from loader import bot
from telebot.types import Message


@bot.message_handler(state=None)
def echo(message: Message) -> None:
    bot.send_message(message.chat.id,
                     'Я не розумію що ви маєте на увазі.\n'
                     f'Ваше повідомлення "{message.text}".')