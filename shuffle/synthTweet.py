import re

import nltk
from nltk.corpus import wordnet as wn
import pandas as pd
from utils import *
import random

nltk.download('omw-1.4')
jikeli = pd.read_excel('jikeliCorpus.xlsx', header=1)
jew = wn.synset('jew.n.01').hyponyms()
print(jew[5].lemmas()[0].name())


def new_tweet(tokens: list[str], ratio=0.25) -> list[str]:
    """replaces @param ratio of tokens in @param tokens with hyponyms and/or synonyms"""
    indices = numpy.random.choice(range(0, len(tokens)), size=int(ratio * len(tokens)))
    tweet = list()
    for index in range(0, len(tokens)):
        if index in indices:
            synonyms = list()
            for segment in wn.synonyms(tokens[index], 'eng'):
                synonyms.extend(segment)
            if wn.synsets(tokens[index]):
                hyponyms = [re.sub("_", " ",hyponym.lemmas()[random.randint(0,len(hyponym.lemmas()) - 1)].name()) for hyponym in wn.synsets(tokens[index])[0].hyponyms()]
            else:
                hyponyms = []
            subs = synonyms + hyponyms
            if subs:
                tweet.append(numpy.random.choice(subs))
            else:
                tweet.append(tokens[index])
        else:
            tweet.append(tokens[index])
    return tweet


tweetIndex = random.randint(0, len(jikeli['Text']) - 1)
print("OLD TWEET: " + jikeli['Text'][tweetIndex])
print(' '.join(new_tweet(clean(jikeli['Text'][tweetIndex]), 0.5)))
