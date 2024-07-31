from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils

# Step 1: Prepare the Data
accounts = utils.load_accounts()

myFinder = CovertLister()
myFinder.classify(accounts)
true_covert = set(read_csv('../../shuffle/covert.csv')['Username'])

feature_list = []
is_positive_list = []
path = 'rfc_account_classifier.pkl'

for account in accounts:
    feature_list.append(investigate_account(myFinder, account.name).append(account.primary_score))
    is_positive_list.append(account.name in true_covert)

build_classifier(feature_list, is_positive_list, path)