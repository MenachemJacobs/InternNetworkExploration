import csv

from AdversaryRevulsion import CovertLister
from Components.Account import Account
from Components.Message import Message

filename = 'shuffle/newData.csv'

Accounts: list["Account"] = []
Overt_accounts: list["Account"] = []
Covert_accounts: list["Account"] = []
Pro_accounts: list["Account"] = []


def read_dataset(file):
    data = []

    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            data.append(row)

    return data


dataset = read_dataset(filename)

for row in dataset[1:]:
    username = row[2]
    text = row[3]
    biased = row[1] == "1"
    new_message = Message(username, text)

    account_found = False

    for i in range(len(Accounts)):
        if Accounts[i].name == username:
            Accounts[i].messages.append(new_message)
            Accounts[i].isAntisemite = Accounts[i].isAntisemite or biased
            account_found = True
            break

    if not account_found:
        Accounts.append(Account(username, [new_message], [], biased))

myFinder = CovertLister()
Covert_accounts = myFinder.uncover_covert(Accounts)
print(myFinder.hot_words)
print(myFinder.hot_phrases)
print(Covert_accounts)
