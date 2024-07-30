import pickle

import pandas as pd


def calculate_secondary_score(account_name: str, feature_list: list) -> float:
    with open('Components/random_forest_classifier.pkl', 'rb') as f:
        loaded_clf = pickle.load(f)

    new_data = pd.DataFrame([feature_list])  # Replace with actual new feature data

    probabilities = loaded_clf.predict_proba(new_data)
    positive_class_prob = probabilities[0, 1]

    print(account_name + ":", positive_class_prob)

    return positive_class_prob


def calculate_messages():
    print()

