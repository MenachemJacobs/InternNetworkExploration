import nltk
from nltk.corpus import wordnet as wn
import pandas as pd
from utils import *
import random
nltk.download('omw-1.4')
jikeli = pd.read_excel('jikeliCorpus.xlsx',header=1)


def new_tweet(tokens: list[str], ratio=0.25):
    tweet = list()

    indices = numpy.random.choice(range(0, len(tokens)), size=int(ratio * len(tokens)))
    for index in range(0,len(tokens)):
        if index in indices:
            synonyms = wn.synonyms(tokens[index],'eng')
            if len(synonyms) > 0:
                if len(synonyms) > 1:
                    synonym_segment = synonyms[random.randint(0, len(synonyms)-1)]
                else:
                    synonym_segment = synonyms[0]
                if len(synonym_segment) > 1:
                    tweet.append(synonym_segment[random.randint(0, len(synonym_segment)-1)])
                elif len(synonym_segment) == 1:
                    tweet.append(synonym_segment[0])
            else:
                continue
        else:
            tweet.append(tokens[index])
    return tweet


tweetIndex = random.randint(0, len(jikeli['Text'])-1)
print("OLD TWEET: " + jikeli['Text'][tweetIndex])
print(' '.join(new_tweet(clean((jikeli['Text'][tweetIndex])))))
