import datetime

import numpy

import hotwords
from Components.Account import *
from ContextGeneration.GenerateNameNetworks import *
import pandas as pd

from shuffle.account_writer import assign_messages_randomly, accounts_to_dataframe
from shuffle.utils import clustered_random_dates, clean, replace_words, insert_bigrams, follower_network

jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)
#initialize network of users
all_users = list(set(jikeli['Username']))
anti_users = set()
pro_users = set()
#prepare message and dates lists
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
    if message.score == 1:
        message.score = random.uniform(0.75, 1)
        anti_users.add(jikeli['Username'][i])
        overt_messages.append(message)
    elif numpy.random.choice((True, False)):
        message.score = random.uniform(0.0, 0.4)
        pro_messages.append(message)
    else:
        message.score = random.uniform(0.0, 0.4)
        tokens = (replace_words(tokens=clean(message.text), replacing=hotwords.hot_words, ratio=0.4))
        tweet = ' '.join(insert_bigrams(tokens=tokens, bigrams=hotwords.hot_phrases, num_insertions=4))
        message.text = tweet
        covert_messages.append(message)
for user in all_users:
    if user not in anti_users:
        pro_users.add(user)
anti_accounts = list()
pro_accounts = list()
covert_accounts = list()
for user in anti_users:
    anti_accounts.append(Account.Account(str(user),list(),list(),True))
for user in pro_users:
    if numpy.random.choice((True, False)):
        pro_accounts.append(Account.Account(user,list(),list(),False))
    else:
        covert_accounts.append(Account.Account(user,list(),list(),False))
#generate account subscriptions
anti_network = follower_network(anti_accounts,anti_accounts,10)
pro_network = follower_network(pro_accounts,pro_accounts,10)
covert_network = follower_network(covert_accounts,pro_accounts + anti_accounts,10)
for account in anti_network.keys():
    account.subscriptions = anti_network[account]
for account in pro_network.keys():
    account.subscriptions = pro_network[account]
for account in covert_network.keys():
    account.subscriptions = covert_network[account]
assign_messages_randomly(covert_accounts[:10] + anti_accounts[:40], covert_messages)
assign_messages_randomly(anti_accounts[:40], overt_messages)
assign_messages_randomly(pro_accounts[:50], pro_messages)
accountData = accounts_to_dataframe(covert_accounts[:10] + pro_accounts[:50] + anti_accounts[:40])
accountData.to_csv('accounts.csv')
