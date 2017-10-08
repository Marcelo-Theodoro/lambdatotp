from datetime import datetime


def log(sender, message):
    time = str(datetime.now())
    print(f'{time} [{sender}]: {message}')
