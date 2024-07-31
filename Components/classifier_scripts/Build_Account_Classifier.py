import pickle

from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils

# Step 1: Prepare the Data
accounts = utils.load_accounts()

# Initialize CovertLister
myFinder = CovertLister()
myFinder.classify(accounts)

with open('../classifiers/rfc_secondary_classifier.pkl', 'rb') as f:
    secondary_clf = pickle.load(f)

for account in accounts:
    account.set_primary_score(accounts, secondary_clf)

# Load the true covert accounts from a CSV file
true_covert = set(read_csv('../../shuffle/covert.csv')['Username'])

# Initialize lists to store features and labels
feature_lists = []
is_positive_list = []
path = 'rfc_account_classifier.pkl'

# Extract features and labels for each account
for account in accounts:
    features: list[float] = investigate_account(myFinder, account.name)
    features.append(float(account.primary_score))
    feature_lists.append(features)
    is_positive_list.append(account.name in true_covert)

counter = 0
for lists in feature_lists:
    if (lists[6] != 0) ^ (lists[7] != 0.0):
        print(list)
    if (lists[6] == 0) and (lists[7] == 0.0):
        counter += 1

print(counter)
build_classifier(feature_lists, is_positive_list, path)
