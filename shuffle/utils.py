import datetime
import string
import pandas as pd
import numpy
import random

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize.casual import TweetTokenizer

stopList = set(stopwords.words('english'))
tokener = TweetTokenizer(strip_handles=True, reduce_len=True)
lem = WordNetLemmatizer()


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
    indices = []
    for index in range(len(arr)):
        if arr[index] == target_value:
            indices.append(index)
    return indices


def jikeli_date(date_text: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S%z')
