import csv

from AdversaryRevulsion import CovertLister
from Components.Account import Account
from Components.Message import Message

filename = 'shuffle/newData.csv'

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

myFinder = CovertLister()
Covert_accounts = myFinder.uncover_covert(Accounts)
# print(myFinder.hot_words[:10])
# print(myFinder.hot_phrases[:10])
# print(Covert_accounts[:10])
for account in myFinder.overt_accounts:
    friend_list = []

    for i in range(len(Accounts)):
        if Accounts[i].name in account.subscriptions:
            friend_list.append(Accounts[i])

    print(account, [(friend.name, friend.isAntisemite) for friend in friend_list])