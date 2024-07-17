from Account import Account
from Crawler import Crawler
from Message import random_message
import GenerateNameNetworks

Alpha = Account("Alpha", random_message(5), []).set_secondary_score()
Bravo = Account("Bravo", random_message(5), []).set_secondary_score()
Charlie = Account("Charlie", random_message(5), []).set_secondary_score()
Delta = Account("Delta", random_message(5), []).set_secondary_score()
Echo = Account("Echo", random_message(5), []).set_secondary_score()
Foxtrot = Account("Foxtrot", random_message(5), []).set_secondary_score()
Golf = Account("Golf", random_message(5), []).set_secondary_score()

Alpha.add_subscriptions([Bravo, Echo])
Bravo.add_subscriptions([Charlie, Echo])
Charlie.add_subscriptions([Delta, Golf])
Delta.add_subscriptions([Bravo, Charlie])
Echo.add_subscriptions([Foxtrot, Golf])
Foxtrot.add_subscriptions([Alpha, Delta])
Golf.add_subscriptions([Alpha, Charlie])

Alpha.set_primary_score()
Bravo.set_primary_score()
Charlie.set_primary_score()
Delta.set_primary_score()
Foxtrot.set_primary_score()
Golf.set_primary_score()

myCrawler = Crawler()

returned_graph = myCrawler.find_neighbors(Alpha, 4)


def dfs_getter(lst):
    return_val = []
    if isinstance(lst, list):
        for item in lst:
            return_val.extend(dfs_getter(item))  # Recursively get sorted elements
    else:
        return_val.append(lst)  # Append leaf nodes (non-list elements)
    return return_val


# print(dfs_getter(returned_graph))
generate_overtlist(dfs_getter(returned_graph))
