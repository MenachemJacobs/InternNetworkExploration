from Components.classifier_scripts.Classifier_Builder_Template import build_classifier
from shuffle import utils

# Step 1: Prepare the Data
accounts = utils.load_training_accounts()

feature_list = []
is_positive_list = []
path = 'rfc_secondary_classifier.pkl'

for account in accounts:
    feature_list.append(account.feature_list)
    is_positive_list.append(account.isAntisemite)

build_classifier(feature_list, is_positive_list, path)
