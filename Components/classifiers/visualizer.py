import pickle

import matplotlib.pyplot as plt
import pandas as pd


# feature_names = ['abs_words', 'comp_words', 'abs_phrases', 'comp_phrases', 'abs_dates', 'comp_dates', 'replies']
# feature_names = ['avg score', 'score/day', 'score/density', 'positives/tweet']

def visualize_classifier(directory_address: str, feature_names: list[str]):
    # Assuming clf is your trained RandomForestClassifier and x is your feature DataFrame
    with open(directory_address, 'rb') as f:
        clf = pickle.load(f)

    # Extract feature importance
    importance = clf.feature_importances_

    # Create a DataFrame with feature names and their importance
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance
    }).sort_values(by='Importance', ascending=False)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.gca().invert_yaxis()  # Highest importance at the top
    plt.show()
