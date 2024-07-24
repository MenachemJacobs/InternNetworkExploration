import csv

from AdversaryRevulsion import CovertLister
from Components.Account import Account
from Components.Message import Message

filename = 'shuffle/accounts.csv'

Accounts: list["Account"] = []


def read_dataset(file):
    data = []

    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            data.append(row)

    return data


dataset = read_dataset(filename)

for row in dataset[1:]:
    timestamp = row[0]
    biased = row[1] == "1"
    username = row[2]
    text = row[3]
    users_followed = row[4]

    message = Message(username, text)
    account_found = False

    for i in range(len(Accounts)):
        if Accounts[i].name == username:
            Accounts[i].messages.append(message)
            Accounts[i].isAntisemite = Accounts[i].isAntisemite or biased
            account_found = True
            break

    if not account_found:
        new_account = Account(username, [message], [], biased)
        new_account.subscriptions = row[4]
        Accounts.append(new_account)

# accounts = list()
#
# for row in range(len(dataset['Username'])):
#     messages = [shuffle.utils.list_to_msg(msg) for msg in dataset['Messages'][row]]
#     antisemitic = dataset['Antisemitic'][row]
#     username = dataset['Username'][row]
#     subscriptions = dataset['Subscriptions'][row]
#     accounts.append(Account(name=username, messages=messages, initial_subscriptions=subscriptions,
#                             antisemite=antisemitic))

myFinder = CovertLister()
result = myFinder.classify(accounts)

print(myFinder.hot_words[:10])
print(myFinder.hot_phrases[:10])
print(myFinder.covert_accounts[:10])
