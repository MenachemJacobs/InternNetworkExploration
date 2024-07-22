import datetime
import string

import nltk
import pandas as pd
import numpy
import random

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize.casual import TweetTokenizer

from Components.Message import Message

stopList = set(stopwords.words('english'))
tokener = TweetTokenizer(strip_handles=True, reduce_len=True)
lem = WordNetLemmatizer()


def replace_bigrams(tokens: list[str], replacing: list[tuple[str, str]], ratio=0.25) -> list[str]:
    bigrams = list()
    i = 0
    while i < len(tokens) - 1:
        bigrams.append((tokens[i].lower(),tokens[i+1].lower()))
        i += 2
    if ratio < 0 or ratio > 1:
        raise ValueError("ratio must be between 0 and 1")
    new_tokens = bigrams
    rand_indices = numpy.random.choice(range(len(bigrams)), size=int(ratio * len(bigrams)))
    for index in rand_indices:
        replacement = numpy.random.choice(len(replacing) - 1)
        new_tokens[index] = replacing[replacement]
    single_tokens = list()
    for tup in new_tokens:
        for token in tup:
            single_tokens.append(token)
    return single_tokens


def replace_words(tokens: list[str], replacing: list[str], ratio=0.25):
    """    :param ratio: number of tokens being replaced divided by number of tokens
:param tokens: list of tokens to be partially replaced
    :param replacing: list of tokens to be used as replacements for tokens in replace_words"""
    if ratio < 0 or ratio > 1:
        raise ValueError("ratio must be between 0 and 1")
    new_tokens = tokens
    rand_indices = numpy.random.choice(range(0, len(tokens)), int(ratio * len(tokens)))
    for i in rand_indices:
        new_tokens[i] = numpy.random.choice(replacing).lower()
    return new_tokens


def clean(text: str):
    """returns a list of lemmatized, lower case tokens from the given string with basic punctuation removed"""
    words = list()
    for word in tokener.tokenize(text):
        if word not in string.punctuation:
            words.append(lem.lemmatize(word.lower()))
    return words


def date_range(past: datetime.datetime, numdates: int, years: int) -> list[datetime.datetime]:
    """:param past: the beginning of the time period
    :param numdates: the number of dates in the time period
    :param years: the number of years in the time period"""
    dates = list()
    for i in range(0, numdates):
        dates.append(past + datetime.timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                               minutes=random.randint(0, 60), seconds=random.randint(0, 60)))
    return dates


def clustered_random_dates(past: datetime.datetime, cluster_size: int, num_cluster: int, years=1, remainder=0) -> \
        list[datetime.datetime]:
    """:param past: the beginning of the time period
    :param num_cluster: the number of clusters in the time period
    :param cluster_size: the size of each cluster of date times
    :param years: the number of years in the time period
    :param remainder: the number of non-clustered date times"""
    dates = list()
    for cluster in range(0, num_cluster):
        date = past + datetime.timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                         minutes=random.randint(0, 60), seconds=random.randint(0, 60))
        for element in range(0, cluster_size):
            dates.append(date + datetime.timedelta(minutes=random.randint(0, 59), hours=random.randint(0, 24),
                                                   seconds=random.randint(0, 59)))
    dates.extend(date_range(past, numdates=remainder, years=years))
    return dates


def followers(follower_names: list[str], leader_names: list[str], connectivity=5) -> dict[str, list[str]]:
    """:param follower_names: the names of the followers
    :param leader_names: the usernames that can be followed
    :param connectivity: the number of people each follower follows"""
    following = dict()
    for i in range(0, len(follower_names)):
        following[follower_names[i]] = numpy.random.choice(a=leader_names, size=connectivity, replace=False)
    return following


def replace_names(names: list[str], target: list[str]) -> list[str]:
    """:param names: the names being written in
    :param target: the names being written over"""
    newList = target
    for i in range(len(target)):
        newList[i] = names[random.randint(0, len(names) - 1)]
    return newList


def weight_bag(cluster_size: int, cluster_num, arr: list):
    for cluster in range(0, cluster_size):
        chosen = numpy.random.choice(arr)
        for element in range(0, cluster_num):
            arr.append(chosen)


def store_indices(arr: list, target_value) -> list[int]:
    """returns an array containing all indices in arr containing target_value"""
    indices = []
    for index in range(len(arr)):
        if arr[index] == target_value:
            indices.append(index)
    return indices


def jikeli_date(date_text: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S%z')


def tuple_to_message(data: tuple) -> Message:
    """converts a tuple of length 3 to a message object; @param data should be in date, text score order."""
    msg = Message()
    msg = msg.testing_constructor(data[0], data[1], data[2])
    return msg


def replace_keyword(keyword: str, tokens: list[str], replacing_tokens: list[str]) -> list[str]:
    word = lem.lemmatize(keyword.lower())
    new_tokens = list()
    for token in tokens:
        if lem.lemmatize(token.lower()) == word:
            new_tokens.append(numpy.random.choice(replacing_tokens))
        else:
            new_tokens.append(token)
    return new_tokens
