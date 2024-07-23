import csv
import datetime

import pandas as pd

import shuffle.utils
from shuffle.create_accounts import accountData
from AdversaryRevulsion import CovertLister
from Components.Account import Account
from Components.Message import Message

filename = 'shuffle/accounts.csv'

Accounts: list["Account"] = []
Covert_accounts: list["Account"] = []
# Pro_accounts: list["Account"] = []


def read_dataset(file):
    data = []

    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            data.append(row)

    return data


dataset = accountData
accounts = list()
for row in range(len(dataset['Username'])):
    messages = [shuffle.utils.tuple_to_message(msg) for msg in dataset['Messages'][row]]
    antisemitic = dataset['Antisemitic'][row]
    username = dataset['Username'][row]
    subscriptions = dataset['Subscriptions'][row]
    accounts.append(Account(name=username, messages=messages, initial_subscriptions=subscriptions,antisemite=antisemitic))

myFinder = CovertLister()
result = myFinder.uncover_covert(accounts)
Covert_accounts = list()
for part in result:
    Covert_accounts.append(part[0])
myFinder.compile_hot_lists(Covert_accounts)
print(myFinder.hot_words[:10])
print(myFinder.hot_phrases[:10])
print(Covert_accounts[:10])
