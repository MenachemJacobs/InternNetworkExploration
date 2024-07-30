import math
from datetime import datetime, timedelta

from pandas import DataFrame, read_csv

from Components.Account import Account
from Components.Message import Message
from shuffle.utils import list_to_msg, parse_list_ints

messageData = read_csv('shuffle/trainingMessages.csv')
accountData = read_csv('shuffle/trainingAccounts.csv', converters={'Messages': parse_list_ints})
# Create a dictionary for quick message lookup
messageLookup = {}

for _, row in messageData.iterrows():
    msg_list = [datetime.strptime(row['Date'], "%d-%b-%Y (%H:%M:%S.%f)"),
                row['Text'], row['Score'], row['Username']]
    msg = list_to_msg(msg_list)
    msg.ID = row['ID']
    msg.replying_to = row['Replying_To']
    messageLookup[int(row['ID'])] = msg

# Create accounts
training_accounts = list()
for _, row in accountData.iterrows():
    messages = {messageLookup[index] for index in row['Messages']}
    antisemitic = row['Antisemitic']
    username = row['Username']
    subscriptions = row['Subscriptions']
    training_accounts.append(Account(name=username, messages=messages, initial_subscriptions=subscriptions,
                                     antisemite=antisemitic))


def extract_features(account: Account,log_base: float, threshold: float) -> list[float]:
    msg_set = account.messages
    first_day = min(msg_set, key=lambda m: m.date).date
    last_day = max(msg_set, key=lambda m: m.date).date
    total_days = (last_day - first_day).days
    num_messages = len(msg_set)
    sum_of_scores = 0.0
    num_periods = math.floor(math.log(total_days) / math.log(log_base))
    periods: list[list['Message']] = [[] for _ in range(num_periods)]
    period_length = timedelta(days=total_days / num_periods)
    acceptable = 0.0
    for message in msg_set:
        sum_of_scores += message.score
        period_index = (message.date - first_day) // period_length
        periods[period_index].append(message)
        if message.score < threshold:
            acceptable += 1.0
    flat_list = []
    for period in periods:
        flat_list.extend(period * len(period))
    density = sum_of_scores / len(flat_list)
    avg = sum_of_scores / len(messages)
    by_day = sum_of_scores / total_days
    positivity = acceptable / len(messages)
    return [density,avg,by_day,positivity]

