import hotwords
import pandas
from ContextGeneration.GenerateNameNetworks import *
from Components.Message import Message
from utils import *

new_dates = clustered_random_dates(datetime.datetime(2012, 11, 28, 12, minute=38, second=57), cluster_size=12,
                                   num_cluster=600, remainder=0, years=1)
jikeliCorpus = pandas.read_excel('jikeliCorpus.xlsx', header=1)
anti_tweets = store_indices(jikeliCorpus['Biased'], 1)
pro_tweets = store_indices(jikeliCorpus['Biased'], 0)
mngr = NetworkManager()
mngr.set_overt_list(default_overt_list)
mngr.set_covert_list(default_covert_list)
mngr.set_pro_list(default_pro_list)
mngr.generate_overt_network()
mngr.generate_covert_network()
mngr.generate_pro_network()
for user in mngr.covert_list:
    user.messages = list()
for user in mngr.overt_list:
    user.messages = list()
covert_tweets = list()
for i in pro_tweets[:3000]:
    covert_tweets.append(replace_words(clean(jikeliCorpus['Text'][i]), hotwords.hot_words + hotwords.hot_phrases, 0.4))
for tweet in covert_tweets[:2000]:
    agent = numpy.random.choice(range(0, len(mngr.covert_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = ' '.join(tweet)
    msg.score = random.uniform(0.2,0.5)
    mngr.covert_list[agent[0]].messages.append(msg)
for tweet in covert_tweets[2001:4000]:
    agent = numpy.random.choice(range(0, len(mngr.overt_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = ' '.join(tweet)
    msg.score = random.uniform(0.2,0.5)
    mngr.overt_list[agent[0]].messages.append(msg)
for index in anti_tweets[:2000]:
    tweet = jikeliCorpus['Text'][index]
    agent = numpy.random.choice(range(0, len(mngr.overt_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = tweet
    msg.score = random.uniform(0.75,1.00)
    mngr.overt_list[agent[0]].messages.append(msg)
users = list()
message_list = list()
antisemitic = list()
friends = list()
scores = list()
for user in mngr.covert_list:
    antisemitic.append(user.antisemite)
    users.append(user.name)
    message_list.append([(msg.text, msg.score,msg.date) for msg in user.messages])
    friends.append(user.subscriptions)
for user in mngr.overt_list:
    user.antisemite = True
    antisemitic.append(user.antisemite)
    users.append(user.name)
    message_list.append([(msg.text, msg.score,msg.date) for msg in user.messages])
    friends.append(user.subscriptions)
accounts = pandas.DataFrame({'Username': users, 'Antisemitic': antisemitic, 'Messages': message_list})
accounts.to_csv('accounts.csv')
