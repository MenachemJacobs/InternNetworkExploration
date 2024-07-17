import re
import string

import numpy.random
import hotwords
import pandas
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from GenerateNameNetworks import *
from Message import Message
from order_utils import *
from Account import Account

tokener = TweetTokenizer(strip_handles=True, reduce_len=True)
lem = WordNetLemmatizer()
new_dates = clustered_random_dates(datetime.datetime(2012, 11, 28, 12, minute=38, second=57), cluster_size=12,
                                   num_cluster=600, remainder=0, years=1)


def replace_words(tokens: list[str], replacing: list[str], ratio=0.25):
    if ratio < 0 or ratio > 1:
        raise ValueError("ratio must be between 0 and 1")
    new_tokens = tokens
    rand_indices = numpy.random.choice(range(0, len(tokens)), int(ratio * len(tokens)))
    for i in rand_indices:
        new_tokens[i] = numpy.random.choice(replacing)
    return new_tokens


def clean(text: str):
    words = list()
    for word in tokener.tokenize(text):
        if word not in string.punctuation:
            words.append(lem.lemmatize(word.lower()))
    return words


jikeliCorpus = pandas.read_excel('jikeliCorpus.xlsx', header=1)
anti_tweets = store_indices(jikeliCorpus['Biased'], 1)
pro_tweets = store_indices(jikeliCorpus['Biased'], 0)
generate_overt_network()
generate_overt_network()
for user in covert_list:
    user.messages = list()
for user in overt_list:
    user.messages = list()
covert_tweets = list()
for i in pro_tweets[:4000]:
    covert_tweets.append(replace_words(clean(jikeliCorpus['Text'][i]), hotwords.hot_words + hotwords.hot_phrases, 0.4))
for tweet in covert_tweets[:2000]:
    agent = numpy.random.choice(range(0, len(covert_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = ' '.join(tweet)
    msg.score = 0
    covert_list[agent[0]].messages.append(msg)
for tweet in covert_tweets[2001:4000]:
    agent = numpy.random.choice(range(0, len(overt_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = ' '.join(tweet)
    msg.score = 0
    overt_list[agent[0]].messages.append(msg)
for index in anti_tweets[:2000]:
    tweet = jikeliCorpus['Text'][index]
    agent = numpy.random.choice(range(0, len(overt_list)), size=1)
    rand_date = new_dates[random.choice(range(0, len(new_dates)))]
    msg = Message()
    msg.date = rand_date
    msg.text = tweet
    msg.score = 1
    overt_list[agent[0]].messages.append(msg)
users = list()
message_list = list()
antisemitic = list()
friends = list()
scores = list()
for user in covert_list:
    antisemitic.append(user.antisemite)
    users.append(user.name)
    message_list.append([msg.text for msg in user.messages])
    friends.append(user.subscriptions)
for user in overt_list:
    user.antisemite = True
    antisemitic.append(user.antisemite)
    users.append(user.name)
    message_list.append([msg.text for msg in user.messages])
    friends.append(user.subscriptions)
accounts = pandas.DataFrame({'Username': users, 'Antisemitic': antisemitic, 'Messages': message_list})
accounts.to_csv('accounts.csv')
