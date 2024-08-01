import json
import pickle
from pathlib import Path

from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils
from Synthesize.synthesize_accounts import train_accounts


def build_account_classifier():
    """Builds the account classifier and pickles it in the classifiers directory"""
    json_path = Path(__file__).parent.parent.parent / 'has_run.json'
    with open(json_path, 'r') as f:
        flags: dict = json.load(f)
        f.close()
    if 'training_accounts' not in flags.keys() or not flags['training_accounts']:
        train_accounts()
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
    path = '../classifiers/rfc_account_classifier.pkl'

    # Extract features and labels for each account
    for account in accounts:
        features: list[float] = investigate_account(myFinder, account.name)
        features.append(float(account.primary_score))
        feature_lists.append(features)
        is_positive_list.append(account.name in true_covert)

    wink_counter = 0
    eyes_counter = 0
    for lists in feature_lists:
        if (lists[6] == 0) and (lists[7] != 0.0):
            wink_counter += 1
        if (lists[6] == 0) and (lists[7] == 0.0):
            eyes_counter += 1

    print("eyes", eyes_counter, "winks", wink_counter)
    build_classifier(feature_lists, is_positive_list, path)
    with open(json_path, 'w') as f:
        flags['account_classifier'] = True
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    build_account_classifier()
