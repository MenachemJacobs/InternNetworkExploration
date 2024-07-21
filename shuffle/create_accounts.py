import datetime

import numpy

import hotwords
from Components.Account import *
from ContextGeneration.GenerateNameNetworks import *
import pandas as pd

from shuffle.account_writer import assign_messages_randomly, accounts_to_dataframe
from shuffle.utils import clustered_random_dates, clean, replace_words

jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)
mngr = NetworkManager()
#initialize network of users
mngr.set_covert_list(default_covert_list)
mngr.set_overt_list(default_overt_list)
mngr.set_pro_list(default_pro_list)
mngr.generate_overt_network()
mngr.generate_pro_network()
mngr.generate_covert_network()

for user in mngr.covert_list:
    user.isAntisemite = False
for user in mngr.overt_list:
    user.isAntisemite = True
for user in mngr.pro_list:
    user.isAntisemite = False

#prepare message and dates lists
overt_messages = list()
pro_messages = list()
covert_messages = list()
dates = clustered_random_dates(datetime.datetime(2012,6,15,11,36,24), cluster_size=10,num_cluster=1130,remainder=11)
for i in range(0, len(jikeli['Text'])):
    message = Message()
    message.score = jikeli['Biased'][i]
    message.text = jikeli['Text'][i]
    message.date = dates[i]
    if message.score == 1:
        message.score = random.uniform(0.75, 1)
        overt_messages.append(message)
    elif numpy.random.choice((True, False)):
        message.score = random.uniform(0.0, 0.4)
        pro_messages.append(message)
    else:
        message.score = random.uniform(0.0, 0.4)
        tweet = ' '.join(replace_words(tokens=clean(message.text), replacing=hotwords.hot_words,ratio=0.5))
        message.text = tweet
        covert_messages.append(message)
assign_messages_randomly(mngr.overt_list + mngr.covert_list, covert_messages)
assign_messages_randomly(mngr.overt_list, overt_messages)
assign_messages_randomly(mngr.pro_list, pro_messages)
accountData = accounts_to_dataframe(mngr.pro_list + mngr.overt_list + mngr.covert_list)
accountData.to_csv('accounts.csv')
