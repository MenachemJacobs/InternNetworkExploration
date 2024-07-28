import csv
import datetime

from pandas import read_csv
from shuffle.utils import list_to_msg, parse_single_int, parse_list_ints

from AdversaryRevulsion import CovertLister
from Components.Account import Account

Accounts: list["Account"] = []


def read_dataset(file):
    data = []

    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            data.append(row)

    return data


messageData = read_csv('shuffle/messages.csv', converters={'Replying_To': parse_single_int})
accountData = read_csv('shuffle/accounts.csv', converters={'Messages': parse_list_ints})
accounts = set()
messageLookup = dict()

for row in range(len(messageData['ID'])):
    msg_list = [datetime.datetime.strptime(messageData['Date'][row], "%d-%b-%Y (%H:%M:%S.%f)"),
                messageData['Text'][row], messageData['Score'][row], messageData['Username'][row]]
    msg = list_to_msg(msg_list)
    msg.ID = messageData['ID'][row]
    msg.replying_to = messageData['Replying_To'][row]
    messageLookup[int(messageData['ID'][row])] = msg

for row in range(len(accountData['Username'])):
    messages = set()
    for index in accountData['Messages'][row]:
        messages.add(messageLookup[index])

    antisemitic = accountData['Antisemitic'][row]
    username = accountData['Username'][row]
    subscriptions = accountData['Subscriptions'][row]
    accounts.add(Account(name=username, messages=messages, initial_subscriptions=subscriptions,
                         antisemite=antisemitic))

myFinder = CovertLister()
myFinder.classify(accounts)
print(myFinder.absolute_hot_words[:10])
print(myFinder.comparative_hot_words[:10])
print(myFinder.absolute_hot_phrases[:10])
print(myFinder.comparative_hot_phrases[:10])
print(myFinder.covert_accounts[:10])
print(myFinder.absolute_hot_dates)
print(myFinder.comparative_hot_dates)
# precision = 0
# total = 0
# gold = pd.read_csv('shuffle/covert.csv')
# covert_gold = set(gold['Username'])
#
# for account in myFinder.covert_accounts[:10]:
#     if account.name in covert_gold:
#         precision += 1
#     total += 1
#
# print(float(precision) / float(total))
