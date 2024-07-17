import random


class ReducedAccount:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def create_accounts_by_bulk(names):
    return [ReducedAccount(name) for name in names]


Rando = ReducedAccount("Randos")

# Default names
covert_list = create_accounts_by_bulk([
    "Michael", "James", "John", "Robert", "William",
    "David", "Richard", "Joseph", "Christopher", "Daniel"
])


def set_covert_list(covert_accounts):
    global covert_list

    if len(covert_accounts) < 10:
        covert_list = covert_accounts.extend(covert_list[(10 - len(covert_accounts)):])
    if len(covert_accounts) >= 10:
        covert_list = covert_accounts[10:]


def generate_covert_network():
    global covert_list

    group_lead = [covert_list[0], covert_list[1]]
    group_michael = [covert_list[2], covert_list[3], covert_list[4]]
    group_william = [covert_list[5], covert_list[6], covert_list[7]]
    group_unis = [covert_list[8], covert_list[9]]

    for lead in group_lead:
        lead.friends.append(Rando)

    for friend in group_michael + group_unis:
        friend.friends.append(covert_list[0])

    for friend in group_william + group_unis:
        friend.friends.append(covert_list[1])


# Default names
overt_list = create_accounts_by_bulk([
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

# If fewer than 40 names are passed, use default names.
# If more than 40 names are passed, use the first 40 names
def set_overt_list(overt_accounts):
    global overt_list

    if len(overt_accounts) < 40:
        overt_list = overt_accounts.extend(covert_list[(40 - len(overt_accounts)):])
    if len(overt_accounts) >= 40:
        overt_list = overt_accounts[40:]

# Function to generate random subset of entries from femail_list up to a given index
def random_subset(number):
    return_val = []
    user_sublist = overt_list[:number]

    # The number of entries to return
    friend_count = random.randint(1, number)

    for _ in range(friend_count):
        random_index = random.randrange(len(user_sublist))
        return_val.append(user_sublist[random_index])
        # Prevent double picking by removing selection
        del user_sublist[random_index]

    return return_val

def generate_overt_network():
    # Assigning friends to overt accounts based on specific rules
    for i in range(len(overt_list)):
        if i < 2:
            overt_list[i].friends.append(Rando)
        else:
            overt_list[i].friends.extend(random_subset(i))

    for name in overt_list:
        print(name.name + ":", name.friends)
