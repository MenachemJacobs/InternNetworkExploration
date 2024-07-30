import math
from datetime import datetime, timedelta

from pandas import read_csv

from Components.Account import Account
from Components.Message import Message
from shuffle import utils
from shuffle.utils import list_to_msg, parse_list_ints

messageData = read_csv('shuffle/trainingMessages.csv')
accountData = read_csv('shuffle/trainingAccounts.csv', converters={'Messages': parse_list_ints})
# Create a dictionary for quick message lookup
training_accounts = utils.load_accounts()


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
