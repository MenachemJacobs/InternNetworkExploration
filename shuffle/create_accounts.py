import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import injectionValues
from utils import *
path = Path(__file__).parent.parent / "Components/classifier_scripts/vectorizer.pkl"
path = path.relative_to(Path.cwd(), walk_up=True)
with open(path, 'rb') as f:
    vectorizer: TfidfVectorizer = pickle.load(f)

path = Path(__file__).parent.parent / "Components/classifier_scripts/rfc_message_classifier.pkl"
path = path.relative_to(Path.cwd(), walk_up=True)
path = path.absolute()
with open(path, 'rb') as f:
    clf: RandomForestClassifier = pickle.load(f)
    print(clf.classes_)
# Read Excel file
jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)
vectors = vectorizer.transform(jikeli['Text'])
# initialize network of users
all_users = list(set(jikeli['Username']))
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
        if numpy.random.choice([True, False]):
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, num_insertions=1))
            message.text = tweet
        overt_messages.add(message)
    elif numpy.random.choice([True, True, True, False]):
        if numpy.random.choice([True, False, False, False, False]):
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, num_insertions=1))
            message.text = tweet
        pro_messages.add(message)
    else:
        if jikeli['Username'][i] not in anti_users and jikeli['Username'][i] not in pro_users:
            covert_users.add(jikeli['Username'][i])
        tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
        tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, num_insertions=1))
        message.text = tweet
        covert_messages.add(message)
for user in users.keys():
    if users[user] >= 2:
        anti_users.add(user)
    elif numpy.random.choice([True, True, True, False]):
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
anti_network = follower_network(anti_accounts[:40], anti_accounts[:40], 10)
pro_network = follower_network(pro_accounts[:50], pro_accounts[:50], 10)
covert_network = follower_network(covert_accounts[:10], pro_accounts[:50] + anti_accounts[:40], 10)

for account in anti_network.keys():
    account.subscriptions = set(anti_network[account])
for account in pro_network.keys():
    account.subscriptions = set(pro_network[account])
for account in covert_network.keys():
    account.subscriptions = set(covert_network[account])
anti_network_2 = follower_network(anti_accounts[40:80], anti_accounts[40:80], 10)
pro_network_2 = follower_network(pro_accounts[50:100], pro_accounts[50:100], 10)
covert_network_2 = follower_network(covert_accounts[10:20], pro_accounts[50:100] + anti_accounts[40:80], 10)

for account in anti_network_2.keys():
    account.subscriptions = anti_network_2[account]
for account in pro_network_2.keys():
    account.subscriptions = pro_network_2[account]
for account in covert_network_2.keys():
    account.subscriptions = covert_network_2[account]
overt_msg_list = list(overt_messages)
pro_msg_list = list(pro_messages)
first_overt = set(overt_msg_list[:int(len(overt_msg_list) / 2)])
second_overt = set(overt_msg_list[int(len(overt_msg_list) / 2):])
first_pro = set(pro_msg_list[:int(len(pro_msg_list) / 2)])
second_pro = set(pro_msg_list[int(len(pro_msg_list) / 2):])
# Assign messages and replies randomly

assign_messages_randomly(covert_accounts[:10] + anti_accounts[:40], covert_messages)

assign_messages_randomly(anti_accounts[:40], first_overt)
assign_messages_randomly(anti_accounts[40:80], second_overt)
assign_messages_randomly(pro_accounts[:50], first_pro)
assign_messages_randomly(pro_accounts[50:100], second_pro)

reply_net(set(covert_accounts[:10] + anti_accounts[:40]), sub_proba=0.5,ratio=0.7)
reply_net(set(anti_accounts[:40] + pro_accounts[:20]), sub_proba=0.5,ratio=0.7)
reply_net(set(pro_accounts[:50] + anti_accounts[:25]), sub_proba=0.5,ratio=0.7)
# Save data tables to CSV
covertList = pd.DataFrame({'Username': [account.name for account in covert_accounts[:10]]})
accountData = accounts_to_dataframe(covert_accounts[:10] + pro_accounts[:50] + anti_accounts[:40])
covert_messages = replace_msg_dates(messages=covert_messages,
                                    dates=injectionValues.dates,
                                    ratio=0.01)
overt_messages = replace_msg_dates(messages=overt_messages, dates=injectionValues.dates,ratio=0.05)
pro_messages = replace_msg_dates(messages=pro_messages, dates=injectionValues.dates,ratio=0.005)
messageData = messages_to_dataframe(covert_messages.union(first_pro.union(first_overt)))
messageData.index.name = 'Index'
accountData.index.name = 'Index'
covertList.index.name = 'Index'
messageData.to_csv('messages.csv')
accountData.to_csv('accounts.csv')
covertList.to_csv('covert.csv')
