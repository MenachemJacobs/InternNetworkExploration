import injectionValues
from utils import *

# Read Excel file
jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)

# initialize network of users
all_users = list(set(jikeli['Username']))
anti_users = set()
covert_users = set()
pro_users = set()

# prepare message and dates lists
overt_messages = set()
pro_messages = set()
covert_messages = set()
dates = clustered_random_dates(datetime(2012, 6, 15, 11, 36, 24), cluster_size=10, num_cluster=1130,
                               remainder=11)
anti_accounts = list()
covert_accounts = list()
pro_accounts = list()
for i in range(0, len(jikeli['Text'])):
    message = Message()
    message.score = jikeli['Biased'][i]
    message.text = jikeli['Text'][i]
    message.date = dates[i]
    message.ID = jikeli['ID'][i]

    if message.score == 1:
        message.score = random.uniform(0.75, 1)
        anti_users.add(jikeli['Username'][i])
        if numpy.random.choice((True, False)):
            tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
            tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, num_insertions=1))
            message.text = tweet
        overt_messages.add(message)
    elif numpy.random.choice((True, True, True, False)):
        pro_users.add(jikeli['Username'][i])
        message.score = random.uniform(0.0, 0.4)
        pro_messages.add(message)
    else:
        covert_users.add(jikeli['Username'][i])
        message.score = random.uniform(0.0, 0.4)
        tokens = (replace_words(tokens=clean(message.text), replacing=injectionValues.hot_words, ratio=0.05))
        tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=injectionValues.hot_phrases, num_insertions=1))
        message.text = tweet
        covert_messages.add(message)

# Create account objects

for user in anti_users:
    anti_accounts.append(Account(str(user), set(), list(), True))
for user in pro_users:
    pro_accounts.append(Account(user, set(), list(), False))
for user in covert_users:
    covert_accounts.append(Account(str(user), set(), list(), False))

# generate account subscriptions
anti_network = follower_network(anti_accounts, anti_accounts, 10)
pro_network = follower_network(pro_accounts, pro_accounts, 10)
covert_network = follower_network(covert_accounts, pro_accounts + anti_accounts, 10)

for account in anti_network.keys():
    account.subscriptions = anti_network[account]
for account in pro_network.keys():
    account.subscriptions = pro_network[account]
for account in covert_network.keys():
    account.subscriptions = covert_network[account]

overt_msg_list = list(overt_messages)
pro_msg_list = list(pro_messages)
first_overt = set(overt_msg_list[:int(len(overt_msg_list)/2)])
second_overt = set(overt_msg_list[int(len(overt_msg_list)/2):])
first_pro = set(pro_msg_list[:int(len(pro_msg_list)/2)])
second_pro = set(pro_msg_list[int(len(pro_msg_list)/2):])
# Assign messages and replies randomly
assign_messages_randomly(covert_accounts[:10] + anti_accounts[:40], covert_messages)
assign_messages_randomly(anti_accounts[:40], first_overt)
assign_messages_randomly(anti_accounts[40:80], second_overt)
assign_messages_randomly(pro_accounts[:50], first_pro)
assign_messages_randomly(pro_accounts[50:100], second_pro)
reply_net(covert_messages, covert_accounts[:10] + anti_accounts[:40], 6)
reply_net(first_overt, anti_accounts[:40] + pro_accounts[:20], 6)
reply_net(second_overt, anti_accounts[40:80] + pro_accounts[50:70], 6)
reply_net(first_pro, pro_accounts[:50] + anti_accounts[:25], 6)
reply_net(second_pro, pro_accounts[50:100] + anti_accounts[40:65], 6)
# Save data tables to CSV
covertList = pd.DataFrame({'Username': [account.name for account in covert_accounts[:10]]})
accountData = accounts_to_dataframe(covert_accounts[:10] + pro_accounts[:50] + anti_accounts[:40])
traininingData = accounts_to_dataframe(pro_accounts[50:100] + anti_accounts[40:80])
covert_messages = replace_msg_dates(messages=covert_messages,
                                    dates=[datetime(2012, 1, 18), datetime(2012, 7, 15), datetime(2012, 8, 16)],
                                    ratio=0.005)
overt_messages = replace_msg_dates(messages=overt_messages,
                                   dates=[datetime(2012, 1, 18), datetime(2012, 7, 15), datetime(2012, 8, 16)],
                                   ratio=0.05)
messageData = messages_to_dataframe(covert_messages.union(pro_messages.union(overt_messages)))
messageData.sort_values(by='ID', inplace=True)

messageData.index.name = 'Index'
accountData.index.name = 'Index'
covertList.index.name = 'Index'
traininingData.index.name = 'Index'

messageData.to_csv('messages.csv')
accountData.to_csv('accounts.csv')
traininingData.to_csv('trainining.csv')
covertList.to_csv('covert.csv')
