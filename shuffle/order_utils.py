import datetime

import pandas as pd
import numpy
import random


def date_range(past: datetime.datetime, numdates: int, years: int) -> list[datetime.datetime]:
    dates = list()
    for i in range(0, numdates):
        dates.append(past + datetime.timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                               minutes=random.randint(0, 60), seconds=random.randint(0, 60)))
    return dates


def clustered_random_dates(past: datetime.datetime, cluster_size: int, num_cluster: int, years: int, remainder=0) -> \
list[datetime.datetime]:
    dates = list()
    for cluster in range(0, num_cluster):
        date = past + datetime.timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                         minutes=random.randint(0, 60), seconds=random.randint(0, 60))
        for element in range(0, cluster_size):
            dates.append(date + datetime.timedelta(minutes=random.randint(0, 59), hours=random.randint(0, 24),
                                                   seconds=random.randint(0, 59)))
    dates.extend(date_range(past, numdates=remainder, years=years))
    return dates


def followers(names: list[str]) -> dict[str, list[str]]:
    follower_list = dict()
    for i in range(0, len(names)):
        follower_list[names[i]] = (numpy.random.choice(a=names, size=random.randint(3, 8), replace=False))
    return follower_list


def replace_names(names: list[str], target: list[str]) -> list[str]:
    for i in range(len(target)):
        target[i] = names[random.randint(0, len(names) - 1)]
    return target


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
