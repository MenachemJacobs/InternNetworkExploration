Overview
This project involves an internship initiative that utilized an existing dataset to synthesize new data and train a bot to identify key features using Python's Natural Language Toolkit (NLTK). The system is designed for natural language processing (NLP) tasks, including feature extraction and data augmentation.

Features
Data Synthesis: Generates new data based on patterns and structures in the original dataset.
Feature Extraction: Trains a bot to identify key features from textual data.
Natural Language Processing: Utilizes NLTK for tokenization, stemming, lemmatization, and feature tagging.

Architecture
Dataset Preparation:
Preprocess the input dataset by cleaning, normalizing, and tokenizing text data.
Applies data augmentation techniques to create synthesized data for model training.

Bot Training
Trains the bot using supervised learning models on the augmented dataset.
Use NLTK to extract linguistic features like part-of-speech tags, named entities, and n-grams.

Feature Identification
Implement algorithms to identify and rank key features based on their relevance to the task.
Output results in a structured format for further analysis.

Additional Efforts
To enhance the system's predictive capabilities, an attempt was made to create a comprehensive feature set from the expanded dataset.
This feature set was then used to train a Random Forest Classifier aimed at identifying and scoring additional data.
The ultimate goal of this effort was to enable hidden adversary detection by leveraging patterns present in human-scored data.
The bot analyzed these patterns to assign scores to new data and new users, effectively flagging potential adversarial entities based on their alignment with identified characteristics.

This project was a collaboration between Ariel Cann and Menachem Jacobs
