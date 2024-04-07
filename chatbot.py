import requests

bot_token = '7061578843:AAH57p4NPAyeruvYYyO_uZ_Mr5kuCMffiKA'
chat_id = '6791675554'

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'


def send(message):
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
