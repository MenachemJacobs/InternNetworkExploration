
from pandas import DataFrame
import hotwords
from shuffle.utils import *
tokener = TweetTokenizer()
# Read Excel file
jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)

# initialize network of users
all_users = list(set(jikeli['Username']))
anti_users = set()
pro_users = set()

# prepare message and dates lists
overt_messages = list()
pro_messages = list()
covert_messages = list()
dates = clustered_random_dates(datetime.datetime(2012, 6, 15, 11, 36, 24), cluster_size=10, num_cluster=1130,
                               remainder=11)
for i in range(0, len(jikeli['Text'])):
    message = Message()
    message.score = jikeli['Biased'][i]
    message.text = jikeli['Text'][i]
    message.date = dates[i]
    message.ID = jikeli['ID'][i]
    if message.score == 1:
        message.score = random.uniform(0.75, 1)
        anti_users.add(jikeli['Username'][i])
        overt_messages.append(message)
    elif numpy.random.choice((True, False)):
        message.score = random.uniform(0.0, 0.4)
        pro_messages.append(message)
    else:
        message.score = random.uniform(0.0, 0.4)
        tokens = (replace_words(tokens=tokener.tokenize(message.text), replacing=hotwords.hot_words, ratio=0.4))
        tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=hotwords.hot_phrases, num_insertions=4))
        message.text = tweet
        covert_messages.append(message)

for user in all_users:
    if user not in anti_users:
        pro_users.add(user)

# Create account objects
anti_accounts = list()
pro_accounts = list()
covert_accounts = list()

for user in anti_users:
    anti_accounts.append(Account(str(user), list(), list(), True))
for user in pro_users:
    if numpy.random.choice((True, False)):
        pro_accounts.append(Account(user, list(), list(), False))
    else:
        covert_accounts.append(Account(user, list(), list(), False))

# generate account subscriptions
anti_network = follower_network(anti_accounts, anti_accounts, 10)
pro_network = follower_network(pro_accounts, pro_accounts, 10)
covert_network = follower_network(covert_accounts, pro_accounts + anti_accounts, 10)
covert_users = list()
for account in anti_network.keys():
    account.subscriptions = anti_network[account]
for account in pro_network.keys():
    account.subscriptions = pro_network[account]
for account in covert_network.keys():
    covert_users.append(account.name)
    account.subscriptions = covert_network[account]

# Assign messages randomly
assign_messages_randomly(covert_accounts[:10] + anti_accounts[:40], covert_messages)
assign_messages_randomly(anti_accounts[:40], overt_messages)
assign_messages_randomly(pro_accounts[:50], pro_messages)
reply_net(covert_messages, covert_accounts, 6)
reply_net(overt_messages,covert_accounts, 6)
reply_net(pro_messages, pro_accounts,6)
# Save data tables to CSV
covertList = pd.DataFrame({'Username': covert_users[:10]})
accountData = accounts_to_dataframe(covert_accounts[:10] + pro_accounts[:50] + anti_accounts[:40])
messageData = messages_to_dataframe(covert_messages + pro_messages + overt_messages)
messageData.sort_values(by='ID',inplace=True)
messageData.to_csv('messages.csv')
accountData.to_csv('accounts.csv')
covertList.to_csv('covert.csv')
