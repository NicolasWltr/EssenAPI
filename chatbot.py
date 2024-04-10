import requests
from BotCreds import bot_token, chat_id

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'


def send(message):
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
