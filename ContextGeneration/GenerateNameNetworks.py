import random
from Components import Account
from Components.Account import random_account, create_accounts_by_bulk

Rando = random_account("Randos")

# Default names
default_covert_list = create_accounts_by_bulk([
    "Michael", "James", "John", "Robert", "William",
    "David", "Richard", "Joseph", "Christopher", "Daniel"
])
# Default names
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

ideal_covert_size = 10
ideal_overt_size = 40


# Function to generate random subset of entries from overt_list up to a given index
def random_subset(number: int) -> list["Account"]:
    return_val = []
    user_sublist = default_overt_list[:number]

    # The number of entries to return
    friend_count = random.randint(1, number)

    for _ in range(friend_count):
        random_index = random.randrange(len(user_sublist))
        return_val.append(user_sublist[random_index])
        # Prevent double picking by removing selection
        del user_sublist[random_index]

    return return_val


class NetworkManager:
    def __init__(self):
        self.covert_list = []
        self.overt_list = []

    # assumes account passed in have no subscription attached. This will be tricky for score counting.
    def set_covert_list(self, passed_accounts: list["Account"]) -> None:
        if len(passed_accounts) < ideal_covert_size:
            self.covert_list = passed_accounts + default_covert_list[:(ideal_covert_size - len(passed_accounts))]
        
        if len(passed_accounts) >= ideal_covert_size:
            self.covert_list = default_covert_list[:ideal_covert_size]

    def generate_covert_network(self):
        group_lead = [self.covert_list[0], self.covert_list[1]]
        group_michael = [self.covert_list[2], self.covert_list[3], self.covert_list[4]]
        group_william = [self.covert_list[5], self.covert_list[6], self.covert_list[7]]
        group_unis = [self.covert_list[8], self.covert_list[9]]

        for lead in group_lead:
            lead.subscriptions.append(Rando)

        for friend in group_michael + group_unis:
            friend.subscriptions.append(self.covert_list[0])

        for friend in group_william + group_unis:
            friend.subscriptions.append(self.covert_list[1])

        return self.covert_list

    # assumes account passed in have no subscription attached. This will be tricky for score counting.
    def set_overt_list(self, passed_accounts: list["Account"]):
        if len(passed_accounts) < ideal_overt_size:
            self.overt_list = passed_accounts + default_overt_list[:(ideal_overt_size - len(default_overt_list))]
        if len(passed_accounts) >= ideal_overt_size:
            self.overt_list = default_overt_list[:ideal_overt_size]

    def generate_overt_network(self):
        # Assigning friends to overt accounts based on specific rules
        for i in range(len(self.overt_list)):
            if i < 2:
                self.overt_list[i].subscriptions.append(Rando)
            else:
                self.overt_list[i].subscriptions.extend(random_subset(i))
                self.overt_list[0].subscriptions.extend(random_subset(10))
                self.overt_list[1].subscriptions.extend(random_subset(10))

        return self.overt_list
