import random
from Account import random_account


def create_accounts_by_bulk(names):
    return [random_account(name) for name in names]


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

class NetworkGenerator:
    def __init__(self):
        self.covert_list = []
        self.overt_list = []


    def set_covert_list(self, passed_accounts):
        if len(passed_accounts) < 10:
            self.covert_list = passed_accounts + default_covert_list[(10 - len(passed_accounts)):]
        if len(passed_accounts) >= 10:
            self.covert_list = default_covert_list[10:]


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


    # If fewer than 40 names are passed, use default names.
    # If more than 40 names are passed, use the first 40 names
    def set_overt_list(self, passed_accounts):
        if len(passed_accounts) < 40:
            self.overt_list = passed_accounts + default_overt_list[(40 - len(default_overt_list)):]
        if len(passed_accounts) >= 40:
            self.overt_list = default_overt_list[40:]


    # Function to generate random subset of entries from femail_list up to a given index
    def random_subset(self, number):
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


    def generate_overt_network(self):
        # Assigning friends to overt accounts based on specific rules
        for i in range(len(self.overt_list)):
            if i < 2:
                self.overt_list[i].subscriptions.append(Rando)
            else:
                self.overt_list[i].subscriptions.extend(self.random_subset(i))

        for name in self.overt_list:
            print(name.name + ":", name.subscriptions)

        return self.overt_list