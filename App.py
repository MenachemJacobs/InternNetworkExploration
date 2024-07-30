import datetime

from pandas import read_csv

from ContextGeneration import Diagnostics
from shuffle.utils import list_to_msg, parse_list_ints

from AdversaryRevulsion import CovertLister
from Components.Account import Account

messageData = read_csv('shuffle/messages.csv')
accountData = read_csv('shuffle/accounts.csv', converters={'Messages': parse_list_ints})

# Create a dictionary for quick message lookup
messageLookup = {}

for _, row in messageData.iterrows():
    msg_list = [datetime.datetime.strptime(row['Date'], "%d-%b-%Y (%H:%M:%S.%f)"),
                row['Text'], row['Score'], row['Username']]
    msg = list_to_msg(msg_list)
    msg.ID = row['ID']
    msg.replying_to = row['Replying_To']
    messageLookup[int(row['ID'])] = msg

# Create accounts
accounts = set()

for _, row in accountData.iterrows():
    messages = {messageLookup[index] for index in row['Messages']}
    antisemitic = row['Antisemitic']
    username = row['Username']
    subscriptions = row['Subscriptions']
    accounts.add(Account(name=username, messages=messages, initial_subscriptions=subscriptions,
                         antisemite=antisemitic))

myFinder = CovertLister()
myFinder.classify(accounts)

gold = read_csv('shuffle/covert.csv')
covert_gold = set(gold['Username'])

for feature in myFinder.feature_set:
    print(feature[:10])

returned_accounts: set = {account[0].name for account in myFinder.covert_accounts[:10]}
print(returned_accounts)

# difference_accounts = returned_accounts - covert_gold
#
# if difference_accounts:
#     first_account = next(iter(difference_accounts))
#     Diagnostics.score_the_man(myFinder, first_account)

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
