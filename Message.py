from datetime import datetime
from random import random


class Message:
    def __init__(self):
        self.ID = 0
        self.username = ""
        self.date = datetime.now()
        self.text = ""
        self.score = random()


