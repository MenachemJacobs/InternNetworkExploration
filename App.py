import pickle
import pandas as pd
from shuffle import utils

secondary_path = 'Components/classifiers/rfc_secondary_classifier.pkl'
account_path = 'Components/classifiers/rfc_account_classifier.pkl'

accounts = utils.load_accounts()
accounts_with_secondary = set['Account']

with open(secondary_path, 'rb') as f:
    secondary_clf = pickle.load(f)

# TODO this is all screwed up. set_primary_accounts needs to be able to see the accounts and this was the best way I
#  could think to do it without duplicating account creation on the other side
all_names = {account.name for account in accounts}

for account in accounts:
    account.set_primary_score(accounts, secondary_clf)
