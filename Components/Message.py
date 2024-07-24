from datetime import datetime, timedelta
from random import randint, random


def random_date() -> datetime:
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
    delta_days = (end_date - start_date).days
    random_days = randint(0, delta_days)

    return start_date + timedelta(days=random_days)


def random_message(num: int) -> list["Message"]:
    return_list = []

    for _ in range(num):
        new_message = Message().testing_constructor(random_date(), "Hello World", random())
        return_list.append(new_message)

    return return_list


class Message:
    def __init__(self, username='', text=''):
        self.ID = 0
        # TODO this should expect an account not a string
        self.username = username
        self.date = datetime.now()
        self.text = text
        self.score = random()
        self.responses: list[int] = []

    def testing_constructor(self, date, text, score) -> "Message":
        self.date: datetime = date
        self.text: str = text
        self.score: int = score

        return self
