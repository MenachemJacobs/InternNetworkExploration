from Account import random_account
from Crawler import Crawler
from GenerateNameNetworks import NetworkGenerator

Alpha = random_account("Alpha").set_secondary_score()
Bravo = random_account("Bravo").set_secondary_score()
Charlie = random_account("Charlie").set_secondary_score()
Delta = random_account("Delta").set_secondary_score()
Echo = random_account("Echo").set_secondary_score()
Foxtrot = random_account("Foxtrot").set_secondary_score()
Golf = random_account("Golf").set_secondary_score()

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
myNetworkGenerator = NetworkGenerator()


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
myNetworkGenerator.set_covert_list(dfs_getter(returned_graph))
print(myNetworkGenerator.generate_covert_network())
