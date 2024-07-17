from Account import create_accounts_by_bulk, random_account
from Crawler import Crawler
from GenerateNameNetworks import NetworkManager

name_list = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf"]
named_friends = create_accounts_by_bulk(name_list)

named_friends[0].add_subscriptions([named_friends[1], named_friends[4]])
named_friends[1].add_subscriptions([named_friends[2], named_friends[4]])
named_friends[2].add_subscriptions([named_friends[3], named_friends[6]])
named_friends[3].add_subscriptions([named_friends[1], named_friends[2]])
named_friends[4].add_subscriptions([named_friends[5], named_friends[6]])
named_friends[5].add_subscriptions([named_friends[0], named_friends[3]])
named_friends[6].add_subscriptions([named_friends[0], named_friends[2]])

for friend in named_friends:
    friend.set_feature_scores()

for friend in named_friends:
    friend.set_primary_score()

myCrawler = Crawler()

returned_graph = myCrawler.find_neighbors(named_friends[0], 4)

def dfs_getter(lst):
    return_val = []
    if isinstance(lst, list):
        for item in lst:
            return_val.extend(dfs_getter(item))  # Recursively get sorted elements
    else:
        return_val.append(lst)  # Append leaf nodes (non-list elements)
    return return_val

returned_graph = dfs_getter(returned_graph)

greek_alphabet = [
    "Alpha", "Beta", "Gamma",
    "Delta", "Epsilon", "Zeta",
    "Eta", "Theta", "Iota",
    "Kappa"
]

hebrew_alphabet = [
    "Aleph", "Beis", "Gimmel",
    "Dalet", "Heiy", "Vav",
    "Zein", "Cheis", "Teis",
    "Yud"
]

greek_friends = create_accounts_by_bulk(greek_alphabet)
hebrew_friends = create_accounts_by_bulk(hebrew_alphabet)

myNetMan = NetworkManager()

myNetMan.set_covert_list(greek_friends)
myNetMan.generate_covert_network()

myNetMan.set_overt_list(hebrew_friends)
myNetMan.generate_overt_network()