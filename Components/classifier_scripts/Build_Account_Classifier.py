import json
import pickle
from pathlib import Path

from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from Components.classifier_scripts.Build_Secondary_Classifier import build_secondary_classifier
from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils


def build_account_classifier():
    """Builds the account classifier and pickles it in the classifiers directory"""
    json_path = Path(__file__).parent.parent.parent / 'has_run.json'
    with open(json_path, 'r') as f:
        flags: dict = json.load(f)
        f.close()
    if 'secondary_classifier' not in flags or not flags['secondary_classifier']:
        build_secondary_classifier()
    # Step 1: Prepare the Data
    accounts = utils.load_accounts()
    # Load the true covert accounts from a CSV file
    true_covert = set(read_csv('../../shuffle/covert.csv')['Username'])
    with open('../classifiers/rfc_secondary_classifier.pkl', 'rb') as f:
        secondary_clf = pickle.load(f)

    for account in accounts:
        account.set_feature_scores()
        account.set_secondary_score(secondary_clf)
        account.set_primary_score(accounts, secondary_clf)

    # Initialize CovertLister
    myFinder = CovertLister()
    myFinder.classify(accounts)
    print(myFinder.absolute_hot_words[:10])
    print(myFinder.absolute_hot_phrases[:10])
    print(myFinder.absolute_hot_dates[:10])
    print(myFinder.comparative_hot_words[:10])
    print(myFinder.comparative_hot_phrases[:10])
    print(myFinder.comparative_hot_dates[:10])




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
        flags['secondary_classifier'] = False
        flags['training_accounts'] = False
        flags['create_accounts'] = False
        flags['message_classifier'] = False
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    build_account_classifier()
