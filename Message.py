# from datetime import datetime
from datetime import datetime
from random import random


class Message:
    def __init__(self):
        self.ID = 0
        self.username = ""
        self.date = datetime.now()
        self.text = ""
        self.score = random()

    def testing_constructor(self, date, text, score):
        self.date = date
        self.text = text
        self.score = score

        return self
