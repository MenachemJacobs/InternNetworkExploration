from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils

# Step 1: Prepare the Data
accounts = utils.load_accounts()

# Initialize CovertLister
myFinder = CovertLister()
myFinder.classify(accounts)

# Load the true covert accounts from a CSV file
true_covert = set(read_csv('../../shuffle/covert.csv')['Username'])

# Initialize lists to store features and labels
feature_lists = []
is_positive_list = []
path = 'rfc_account_classifier.pkl'

# Extract features and labels for each account
for account in accounts:
    features = investigate_account(myFinder, account.name)
    features.append(account.primary_score)
    feature_lists.append(features)
    is_positive_list.append(account.name in true_covert)

build_classifier(feature_lists, is_positive_list, path)
