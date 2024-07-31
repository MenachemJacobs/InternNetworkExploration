from pandas import read_csv

from ContextGeneration import Diagnostics

from AdversaryRevulsion import CovertLister
from shuffle import utils
accounts = utils.load_accounts()

# TODO this is all screwed up. set_primary_accounts needs to be able to see the accounts and this was the best way I
#  could think to do it without duplicating account creation on the other side
all_names = {account.name for account in accounts}
for account in accounts:
    account.set_primary_score(accounts)

myFinder = CovertLister()
myFinder.classify(accounts)

gold = read_csv('shuffle/covert.csv')
covert_gold = set(gold['Username'])

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
