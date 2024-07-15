from Account import Account


class Crawler:

    def __init__(self):
        self.subnetwork = []
        self.network_set = set()

        """
        Find all neighbors of an account up to a given distance.

        Parameters:
        locus (Account): The starting account.
        dist (int): The maximum distance to search for neighbors.

        Returns:
        set: A set of accounts within the given distance.
        """
    def find_neighbors(self, locus: 'Account', dist: int):
        if dist > 0:
            if locus not in self.network_set:
                self.network_set.add(locus)
                self.subnetwork.append(locus)
                for account in locus.get_subscriptions():
                    self.find_neighbors(account, dist - 1)

        return self.subnetwork
