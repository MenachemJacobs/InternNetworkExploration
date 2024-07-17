import re
import string
from nltk.probability import FreqDist
import nltk
import gensim
from gensim.models import word2vec
from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
import pandas
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk import ngrams
from nltk import pos_tag
from nltk.lm import NgramCounter

tokener = TweetTokenizer(strip_handles=True, reduce_len=True)
lem = WordNetLemmatizer()


def clean(text: str):
    words = list()
    for word in tokener.tokenize(text):
        if word not in string.punctuation:
            words.append(lem.lemmatize(word.lower()))
    return words


jikeliCorpus = pandas.read_excel('jikeliCorpus.xlsx', header=1)
