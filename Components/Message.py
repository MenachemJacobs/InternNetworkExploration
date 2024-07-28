from datetime import datetime, timedelta
from random import randint, random


def random_date() -> datetime:
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
    delta_days = (end_date - start_date).days
    random_days = randint(0, delta_days)

    return start_date + timedelta(days=random_days)


def random_message(num: int) -> set["Message"]:
    return_list = set()

    for _ in range(num):
        new_message = Message().testing_constructor(random_date(), "Hello World", random())
        return_list.add(new_message)

    return return_list


class Message:
    def __init__(self, username='', text=''):
        # This is going to be an Account but don't tell the python compiler, or it'll freak out
        self.replying_to = 0
        self.ID = 0
        # TODO this should expect an account not a string
        self.username = username
        self.date = datetime.now()
        self.text = text
        self.score = random()

    def testing_constructor(self, date, text, score) -> "Message":
        self.date: datetime = date
        self.text: str = text
        self.score: int = score

        return self
