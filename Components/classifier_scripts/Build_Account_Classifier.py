import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

from pandas import read_csv

from AdversaryRevulsion import CovertLister, investigate_account
from shuffle import utils

# Step 1: Prepare the Data
accounts = utils.load_accounts()

myFinder = CovertLister()
myFinder.classify(accounts)
true_covert = set(read_csv('../../shuffle/covert.csv')['Username'])

feature_list = []
is_positive_list = []

for account in accounts:
    feature_list.append(investigate_account(myFinder, account.name))
    is_positive_list.append(account.name in true_covert)

# Convert to pandas DataFrame
x = pd.DataFrame(feature_list)
y = pd.Series(is_positive_list)

# Step 2: Split the Data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)

# Step 3: Initialize the RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Step 4: Train the Classifier
clf.fit(X_train, y_train)

# Step 5: Evaluate the Classifier (Optional)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Step 6: Save the Trained Classifier
with open('rfc_account_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

# To Use the saved classifier, simply
# with open('random_forest_classifier.pkl', 'rb') as f:
#     loaded_clf = pickle.load(f)
# new_data = pd.DataFrame(new_feature_list)  # Replace with actual new feature data
# new_predictions = loaded_clf.predict(new_data)
# print(new_predictions)
