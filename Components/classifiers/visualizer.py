import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

account_feature_names = [
    'abs_words', 'comp_words', 'abs_phrases', 'comp_phrases', 'abs_dates', 'comp_dates', 'replies', 'primary score'
]
secondary_feature_names = ['avg score', 'score/day', 'score/density', 'positives/tweet']

account_classifier_address = 'rfc_account_classifier.pkl'
secondary_classifier_address = 'rfc_secondary_classifier.pkl'


def visualize_classifier(directory_address: str, feature_names: list[str]):
    # Load the trained RandomForestClassifier
    with open(directory_address, 'rb') as f:
        clf: RandomForestClassifier = pickle.load(f)

    # Extract feature importance

    importances = clf.feature_importances_
    print(importances)
    # Debug prints
    print(f"Number of features expected: {len(feature_names)}")
    print(f"Number of importances returned by the model: {len(importances)}")

    # Create a DataFrame with feature names and their importance
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.gca().invert_yaxis()  # Highest importance at the top
    plt.show()


visualize_classifier(account_classifier_address, account_feature_names)
visualize_classifier(secondary_classifier_address, secondary_feature_names)
