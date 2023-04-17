from dotenv import load_dotenv, find_dotenv, dotenv_values

if not find_dotenv():
    exit('Бота неможливо запустити, так як відсутній файл .env')
else:
    load_dotenv()

BOT_TOKEN = dotenv_values().get('BOT_TOKEN')
RAPIDAPI_KEY = dotenv_values().get('RAPIDAPI_KEY')

COMMANDS = (
    ('start', 'Запустити бота'),
    ('help', 'Вивести довідку'),
    ('weather', 'Продивитися погоду'),
    ('city', 'Змініти відстежуване місто'),
    ('cancel', 'Повернутися до головного меню'),
)