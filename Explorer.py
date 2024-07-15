from Account import Account
from Crawler import Crawler

Alpha = Account("Alpha")
Bravo = Account("Bravo")
Charlie = Account("Charlie")
Delta = Account("Delta")
Echo = Account("Echo")
Foxtrot = Account("Foxtrot")
Golf = Account("Golf")

Alpha.add_subscriptions([Bravo, Echo])
Bravo.add_subscriptions([Charlie, Echo])
Echo.add_subscriptions([Foxtrot, Golf])

myCrawler = Crawler()

returned_graph = myCrawler.find_neighbors(Alpha, 4)


def dfs_iterative(lst):
    if isinstance(lst, list):
        for item in lst:
            dfs_iterative(item)
    else:
        print(lst)


dfs_iterative(returned_graph)