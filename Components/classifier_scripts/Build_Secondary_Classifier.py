import json
from pathlib import Path

from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils
from shuffle.create_accounts import create_accounts


def build_secondary_classifier():
    """Builds the secondary classifier and pickles it in the classifiers directory"""
    json_path = Path(__file__).parent.parent.parent / 'has_run.json'
    with open(json_path, 'r') as f:
        flags: dict = json.load(f)
        f.close()
    if 'create_accounts' not in flags.keys() or not flags['create_accounts']:
        create_accounts()
    # Step 1: Prepare the Data
    accounts = utils.load_training_accounts()

    feature_list = []
    is_positive_list = []
    path = Path(__file__).parent.parent / 'classifiers/rfc_secondary_classifier.pkl'
    for account in accounts:
        feature_list.append(account.feature_list)
        is_positive_list.append(account.isAntisemite)
    build_classifier(feature_list, is_positive_list, path)
    with open(json_path, 'w') as f:
        flags['secondary_classifier'] = True
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    build_secondary_classifier()