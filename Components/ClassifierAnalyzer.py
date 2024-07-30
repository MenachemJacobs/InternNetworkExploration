import pandas as pd
import pickle
import matplotlib.pyplot as plt


def get_feature_importance() -> None:
    # Load the trained classifier
    with open('random_forest_classifier.pkl', 'rb') as f:
        loaded_clf = pickle.load(f)

    # Get feature importance
    importance = loaded_clf.feature_importances_

    # Assuming you have feature names (e.g., from a DataFrame)
    feature_names = ['avg msg score', 'score/day', 'score/density', 'pos/tweet']
    # Replace with actual feature names

    # Create a DataFrame to display feature importance
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance
    }).sort_values(by='Importance', ascending=False)

    print(feature_importance_df)

    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.gca().invert_yaxis()  # Invert y-axis to have the most important feature at the top
    plt.show()


# Call the function to print and plot feature importance
get_feature_importance()
