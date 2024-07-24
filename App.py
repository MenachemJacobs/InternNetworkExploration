import ast
import csv
import datetime

import pandas as pd
from shuffle.utils import list_to_msg

from AdversaryRevulsion import CovertLister
from Components.Account import Account

accountFile = 'shuffle/accounts.csv'
messageFile = 'shuffle/messages.csv'

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


accountData = pd.read_csv(accountFile, converters={'Messages': ast.literal_eval})
messageData = pd.read_csv(messageFile)
accounts = list()
messageLookup = dict()
for row in range(len(messageData['ID'])):
    msg_list = [datetime.datetime.strptime(messageData['Date'][row], "%d-%b-%Y (%H:%M:%S.%f)"),
                messageData['Text'][row], messageData['Score'][row]]
    msg = list_to_msg(msg_list)
    msg.ID = messageData['ID'][row]
    messageLookup[int(messageData['ID'][row])] = msg
for row in range(len(accountData['Username'])):
    messages = list()
    for index in accountData['Messages'][row]:
        messages.append(messageLookup[index])
    antisemitic = accountData['Antisemitic'][row]
    username = accountData['Username'][row]
    subscriptions = accountData['Subscriptions'][row]
    accounts.append(Account(name=username, messages=messages, initial_subscriptions=subscriptions,
                            antisemite=antisemitic))

myFinder = CovertLister()
result = myFinder.classify(accounts)

Covert_accounts = list()

for part in result:
    Covert_accounts.append(part[0])

print(myFinder.hot_words[:10])
print(myFinder.hot_phrases[:10])
print(Covert_accounts[:10])
