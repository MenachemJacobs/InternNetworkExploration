from datetime import datetime, timedelta
from random import random, randint

from Account import Account
from Crawler import Crawler
from Message import Message


def random_date():
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
    delta_days = (end_date - start_date).days
    random_days = randint(0, delta_days)
    return start_date + timedelta(days=random_days)


def random_message(num: int):
    return_list = []

    for _ in range(num):
        new_message = Message().testing_constructor(random_date(), "Hello World", random())
        return_list.append(new_message)

    return return_list


Alpha = Account("Alpha", random_message(5), []).set_secondary_score()
Bravo = Account("Bravo", random_message(5), []).set_secondary_score()
Charlie = Account("Charlie", random_message(5), []).set_secondary_score()
Delta = Account("Delta", random_message(5), []).set_secondary_score()
Echo = Account("Echo", random_message(5), []).set_secondary_score()
Foxtrot = Account("Foxtrot", random_message(5), []).set_secondary_score()
Golf = Account("Golf", random_message(5), []).set_secondary_score()

Alpha.add_subscriptions([Bravo, Echo])
Bravo.add_subscriptions([Charlie, Echo])
Echo.add_subscriptions([Foxtrot, Golf])

Alpha.set_primary_score()
Bravo.set_primary_score()
Charlie.set_primary_score()
Delta.set_primary_score()
Foxtrot.set_primary_score()
Golf.set_primary_score()

myCrawler = Crawler()

returned_graph = myCrawler.find_neighbors(Alpha, 4)


def dfs_iterative(lst):
    return_val = []

    if isinstance(lst, list):
        for item in lst:
            dfs_iterative(item)
    else:
        print(lst)
        return_val.append(lst)

    return return_val


print(dfs_iterative(returned_graph))