import random
from Components import Account
from Components.Account import random_account, create_accounts_by_bulk

Rando = random_account("Randos")

# Default names for different lists
default_covert_list = create_accounts_by_bulk([
    "Michael", "James", "John", "Robert", "William",
    "David", "Richard", "Joseph", "Christopher", "Daniel"
])
default_overt_list = create_accounts_by_bulk([
    "Alice", "Sophia", "Emma", "Olivia", "Ava",
    "Isabella", "Mia", "Amelia", "Harper", "Evelyn",
    "Abigail", "Emily", "Elizabeth", "Mila", "Ella",
    "Avery", "Sofia", "Camila", "Aria", "Scarlett",
    "Victoria", "Madison", "Luna", "Grace", "Chloe",
    "Penelope", "Layla", "Riley", "Zoey", "Nora",
    "Lily", "Eleanor", "Hannah", "Lillian", "Addison",
    "Aubrey", "Ellie", "Stella", "Natalie", "Zoe",
    "Leah"
])
default_pro_list = create_accounts_by_bulk([
    "Montgomery", "Juneau", "Phoenix", "Little Rock", "Sacramento", "Denver",
    "Hartford", "Dover", "Tallahassee", "Atlanta", "Honolulu", "Boise",
    "Springfield", "Indianapolis", "Des Moines", "Topeka", "Frankfort", "Baton Rouge",
    "Augusta", "Annapolis", "Boston", "Lansing", "Saint Paul", "Jackson",
    "Jefferson City", "Helena", "Lincoln", "Carson City", "Concord", "Trenton",
    "Santa Fe", "Albany", "Raleigh", "Bismarck", "Columbus", "Oklahoma City",
    "Salem", "Harrisburg", "Providence", "Columbia", "Pierre", "Nashville",
    "Austin", "Salt Lake City", "Montpelier", "Richmond", "Olympia", "Charleston",
    "Madison", "Cheyenne"
])

ideal_covert_size = 10
ideal_overt_size = 40
ideal_pro_size = 50


# Function to generate random subset of entries from overt_list up to a given index
def random_from_subset(account_list, number: int) -> list["Account"]:
    if number > len(account_list):
        number = len(account_list)

    user_sublist = account_list[:number]
    # The number of entries to return
    friend_count = random.randint(1, number)

    return random.sample(user_sublist, friend_count)


class NetworkManager:
    def __init__(self):
        self.covert_list: list["Account"] = []
        self.overt_list: list["Account"] = []
        self.pro_list: list["Account"] = []

    def set_list(self, list_name: str, passed_accounts: list["Account"], ideal_size: int,
                 default_list: list[str]):

        if len(passed_accounts) < ideal_size:
            default_accounts = default_list[:(ideal_size - len(passed_accounts))]
            setattr(self, list_name, passed_accounts + default_accounts)
        else:
            setattr(self, list_name, passed_accounts[:ideal_size])

    def set_covert_list(self, passed_accounts: list["Account"]) -> list["Account"]:
        """Set the covert list of accounts."""
        self.set_list("covert_list", passed_accounts, ideal_covert_size, default_covert_list)
        return self.generate_covert_network()

    def set_overt_list(self, passed_accounts: list["Account"]) -> list["Account"]:
        """Set the overt list of accounts."""
        self.set_list("overt_list", passed_accounts, ideal_overt_size, default_overt_list)
        return self.generate_overt_network()

    def set_pro_list(self, passed_accounts: list["Account"]) -> list["Account"]:
        """Set the pro list of accounts."""
        self.set_list("pro_list", passed_accounts, ideal_pro_size, default_pro_list)
        return self.generate_pro_network()

    def generate_covert_network(self) -> list["Account"]:
        """Generate connections in the covert network."""
        group_lead = self.covert_list[:2]
        group_michael = self.covert_list[2:5]
        group_william = self.covert_list[5:8]
        group_unis = self.covert_list[8:10]

        for lead in group_lead:
            lead.subscriptions.append(Rando)

        for friend in group_michael + group_unis:
            friend.subscriptions.append(self.covert_list[0])

        for friend in group_william + group_unis:
            friend.subscriptions.append(self.covert_list[1])

        return self.covert_list

    def generate_overt_network(self) -> list["Account"]:
        """Generate connections in the overt network."""
        # Assigning friends to overt accounts based on specific rules
        for i in range(len(self.overt_list)):
            if i < 2:
                self.overt_list[i].subscriptions.append(Rando)
            else:
                self.overt_list[i].subscriptions.extend(random_from_subset(self.overt_list, i))

        self.overt_list[0].subscriptions.extend(random_from_subset(self.overt_list, 10))
        self.overt_list[1].subscriptions.extend(random_from_subset(self.overt_list, 10))

        return self.overt_list

    def generate_pro_network(self) -> list["Account"]:
        for account in self.pro_list:
            number_friends = random.randint(1, len(self.pro_list) // 2)
            possible_friends = [friend for friend in self.pro_list if friend != account]

            friends = random.sample(possible_friends, number_friends)
            account.subscriptions.extend(friends)

        return self.pro_list
