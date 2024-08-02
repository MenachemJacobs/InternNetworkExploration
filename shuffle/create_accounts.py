import json
import pickle
import random
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from Components.classifier_scripts.Build_Message_Classifier import build_message_classifier
from shuffle import injectionValues
from shuffle.utils import *


def create_accounts():
    json_path = Path(__file__).parent.parent / 'has_run.json'
    with open(json_path, 'r') as f:
        flags: dict = json.load(open(json_path))
        f.close()
    if 'message_classifier' not in flags or flags['message_classifier'] == 'false':
        build_message_classifier()
    path = Path(__file__).parent.parent / "Components/classifier_scripts/vectorizer.pkl"
    path = path.relative_to(Path.cwd(), walk_up=True)
    with open(path, 'rb') as f:
        vectorizer: TfidfVectorizer = pickle.load(f)
        f.close()

    path = Path(__file__).parent.parent / "Components/classifier_scripts/rfc_message_classifier.pkl"
    path = path.relative_to(Path.cwd(), walk_up=True)
    path = path.absolute()
    with open(path, 'rb') as f:
        clf: RandomForestClassifier = pickle.load(f)
        f.close()
        print("label order: ", clf.classes_)
    # Read Excel file
    path = Path(__file__).parent / "jikeliCorpus.xlsx"
    path = path.relative_to(Path.cwd(), walk_up=True)
    path = path.absolute()
    jikeli = pd.read_excel(path, header=1)
    vectors = vectorizer.transform(jikeli['Text'])
    # initialize network of users
    users = dict()
    anti_users, covert_users, pro_users = set(), set(), set()
    overt_messages, pro_messages, covert_messages = set(), set(), set()
    anti_accounts, covert_accounts, pro_accounts = list(), list(), list()
    dates = clustered_random_dates(datetime(2012, 6, 15, 11, 36, 24), cluster_size=10, num_cluster=1130,
                                   remainder=11)

    for i in range(0, len(jikeli['Text'])):
        if jikeli['Username'][i] not in users:
            users[jikeli['Username'][i]] = 0
        message = Message()
        message.score = clf.predict_proba(vectors[i])[0][1]
        message.text = jikeli['Text'][i]
        message.date = dates[i]
        message.ID = jikeli['ID'][i]

        if message.score > 0.5:
            users[jikeli['Username'][i]] += 1
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.1))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, ratio=0.02))
            message.text = tweet
            overt_messages.add(message)
        elif numpy.random.choice([True,True, False]):
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, ratio=0.01))
            message.text = tweet
            pro_messages.add(message)
        else:
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.075))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, ratio=0.015))
            message.text = tweet
            covert_messages.add(message)
    for user in users.keys():
        if users[user] >= 2:
            anti_users.add(user)
        elif numpy.random.choice([True, False]):
            pro_users.add(user)
        else:
            covert_users.add(user)
    # Create account objects
    for user in anti_users:
        anti_accounts.append(Account(str(user), set(), set(), True))
    for user in pro_users:
        pro_accounts.append(Account(str(user), set(), set(), False))
    for user in covert_users:
        covert_accounts.append(Account(str(user), set(), set(), False))
    # generate account subscriptions
    anti_network = follower_network(anti_accounts[:50], anti_accounts[:50] + pro_accounts[:25], 15)
    pro_network = follower_network(pro_accounts[:50], pro_accounts[:50] + anti_accounts[:25], 15)
    covert_network = follower_network(covert_accounts[:50], pro_accounts[:50] + anti_accounts[:50], 15)
    for account in anti_network.keys():
        account.subscriptions = set(anti_network[account])
    for account in pro_network.keys():
        account.subscriptions = set(pro_network[account])
    for account in covert_network.keys():
        account.subscriptions = set(covert_network[account])

    part_pro = set(list(pro_messages)[:len(pro_messages)//2])

# Assign messages and replies randomly
    assign_messages_randomly(pro_accounts[:50], pro_messages - part_pro)
    assign_messages_randomly(covert_accounts[:50], covert_messages)
    assign_messages_randomly(anti_accounts[:50], overt_messages)
    assign_messages_randomly(anti_accounts[:50], part_pro)
    reply_net(set(covert_accounts[:50] + anti_accounts[:50]), sub_proba=0.7, ratio=0.8)
    reply_net(set(anti_accounts[:50] + pro_accounts[:25]), sub_proba=0.7, ratio=0.8)
    reply_net(set(pro_accounts[:50] + anti_accounts[:25]), sub_proba=0.7, ratio=0.8)
    # Save data tables to CSV
    covertList = pd.DataFrame({'Username': [account.name for account in covert_accounts[:50]]})
    accountData = accounts_to_dataframe(covert_accounts[:50] + pro_accounts[:50] + anti_accounts[:50])
    covert_messages = replace_msg_dates(messages=covert_messages,
                                        dates=injectionValues.dates,
                                        ratio=0.04)
    overt_messages = replace_msg_dates(messages=overt_messages, dates=injectionValues.dates, ratio=0.06)
    pro_messages = replace_msg_dates(messages=pro_messages, dates=injectionValues.dates, ratio=0.02)
    messageData = messages_to_dataframe(covert_messages.union(pro_messages.union(overt_messages)))
    messageData.index.name = 'Index'
    accountData.index.name = 'Index'
    covertList.index.name = 'Index'
    path = Path(__file__).parent
    messageData.to_csv(path / 'messages.csv')
    accountData.to_csv(path / 'accounts.csv')
    covertList.to_csv(path / 'covert.csv')
    print("average messages per covert account: ", sum(len(account.messages) for account in covert_accounts[:50])/50)
    print("average messages per pro account: ", sum(len(account.messages) for account in pro_accounts[:50])/50)
    print("average messages per overt account: ", sum(len(account.messages) for account in anti_accounts[:50])/50)
    flags['create_accounts'] = True
    with open(json_path, 'w') as f:
        json.dump(flags, f)
        f.close()


if __name__ == '__main__':
    create_accounts()
