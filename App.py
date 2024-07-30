import datetime

from pandas import read_csv

from ContextGeneration import Diagnostics


from AdversaryRevulsion import CovertLister
from Components.Account import Account
from shuffle import utils

accounts = utils.load_accounts()

myFinder = CovertLister()
myFinder.classify(accounts)

gold = read_csv('shuffle/covert.csv')
covert_gold = set(gold['Username'])

returned_accounts: set = {account[0].name for account in myFinder.covert_accounts[:10]}
print(returned_accounts)

for feature in myFinder.feature_set:
    print(feature[:10])

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
