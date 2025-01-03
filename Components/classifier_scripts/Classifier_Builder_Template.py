# Convert to pandas DataFrame
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split


def build_classifier(feature_lists, is_positive_list, path):
    # Convert to DataFrame and Series
    x = pd.DataFrame(feature_lists)
    y = pd.Series(is_positive_list)

    # Step 2: Split the Data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)

    # Step 3: Initialize the RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Step 4: Train the Classifier
    clf.fit(x_train, y_train)

    # Step 5: Evaluate the Classifier (Optional)
    y_pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print(clf.feature_importances_)

    # Step 6: Save the Trained Classifier
    with open(path, 'wb') as f:
        pickle.dump(clf, f)
        f.close()

    # To Use the saved classifier, simply
    # with open('random_forest_classifier.pkl', 'rb') as f:
    #     loaded_clf = pickle.load(f)
    # new_data = pd.DataFrame(new_feature_list)  # Replace with actual new feature data
    # new_predictions = loaded_clf.predict(new_data)
    # print(new_predictions)
