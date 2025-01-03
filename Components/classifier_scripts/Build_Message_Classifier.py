import json
import pickle
from pathlib import Path

import pandas as pd  # Importing pandas for data manipulation
from sklearn.ensemble import RandomForestClassifier  # Importing Random Forest Classifier
from sklearn.feature_extraction.text import TfidfVectorizer  # For converting text to numerical representation
from sklearn.model_selection import train_test_split  # For splitting data into training and testing sets


def build_message_classifier():
    # Define the path to the Excel file containing the dataset
    path = Path(__file__).parent.parent.parent / "shuffle/jikeliCorpus.xlsx"
    path = path.relative_to(Path.cwd(), walk_up=True)
    path = path.absolute()
    data = pd.read_excel(path, header=1)

    # Define the texts (tweets) and labels (0 = Non-antisemitic, 1 = Antisemitic)
    texts = data['Text']  # "Text" is the column name in the CSV file that contains the tweets
    labels = data['Biased']  # "Biased" is the column name in the CSV file that contains the labels determined by human
    # annotators

    #Convert the text data into numerical values using TF-IDF.
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X = vectorizer.fit_transform(texts)

    # Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)

    random_forest = RandomForestClassifier(n_estimators=100, class_weight='balanced')
    path = Path(__file__).parent
    random_forest.fit(X_train, y_train)
    with open(path / 'rfc_message_classifier.pkl', 'wb') as f:
        pickle.dump(random_forest, f)
    with open(path / 'vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    path = Path(__file__).parent.parent.parent / 'has_run.json'
    with open(path, 'r') as f:
        flags = json.load(f)
        f.close()
    with open(path, 'w') as f:
        flags['message_classifier'] = True
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    build_message_classifier()
