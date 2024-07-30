import os
from datetime import datetime, timedelta
import string

import random

import numpy.random
import pandas as pd
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from pandas import read_csv

from Components.Account import Account
from Components.Message import Message

stopList = set(stopwords.words('english'))
lem = WordNetLemmatizer()
escape = {'\'', '\\', '\n', '\r', '\t', '\b', '\f', '\v'}


def insert_tokens(num_insertions: int, tokens: list[str], inserting: list[str]):
    """Randomly insert :param num_insertions words from list :param inserting into list :param tokens
    and return the list; does not modify list in place."""
    inserted = 0
    new_tokens = tokens.copy()
    while inserted < num_insertions:
        rand_index = random.randint(0, len(tokens) - 1)
        new_tokens.insert(rand_index, numpy.random.choice(inserting))
        inserted += 1
    return new_tokens


def insert_bigrams(num_insertions: int, tokens: list[str], bigrams: list[tuple[str, str]]) -> list[str]:
    """Randomly insert :param num_insertions bigrams from list :param bigrams into list :param tokens and return the
    list; does not modify list in place."""
    new_tokens = tokens.copy()
    for inserted in range(num_insertions):
        rand_index = random.randint(0, len(tokens) - 1)
        bigram_index = numpy.random.choice(range(len(bigrams)))
        rand_bigram = bigrams[bigram_index][0] + " " + bigrams[bigram_index][1]
        new_tokens.insert(rand_index, rand_bigram)
    return new_tokens


def replace_words(tokens: list[str], replacing: list[str], ratio=0.25) -> list[str]:
    """    :param ratio: number of tokens being replaced divided by number of tokens
:param tokens: list of tokens to be partially replaced
    :param replacing: list of tokens to be used as replacements for tokens in replace_words"""
    if ratio < 0 or ratio > 1:
        raise ValueError("ratio must be between 0 and 1")
    new_tokens = tokens.copy()
    rand_indices = numpy.random.choice(range(0, len(tokens)), int(ratio * len(tokens)))
    for i in rand_indices:
        new_tokens[i] = numpy.random.choice(replacing).lower()
    return new_tokens


def clean(text: str):
    """returns a list of lemmatized, lower case tokens from the given string with basic punctuation removed"""
    words = list()
    for word in word_tokenize(text):
        if word not in string.punctuation and word not in escape:
            words.append(word.lower())
    return words


def date_range(past: datetime, numdates: int, years: int) -> list[datetime]:
    """:param past: the beginning of the time period
    :param numdates: the number of dates in the time period
    :param years: the number of years in the time period"""
    dates = list()
    for i in range(0, numdates):
        dates.append(past + timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                      minutes=random.randint(0, 60), seconds=random.randint(0, 60)))
    return dates


def replace_msg_dates(messages: set[Message], dates: list[datetime], ratio=0.25) -> set[Message]:
    """Returns the list of messages with :param ratio of their dates replaced with new :param dates"""
    new_messages = list(messages)
    if ratio < 0 or ratio > 1:
        raise ValueError("ratio must be between 0 and 1")
    num_replacements = int(ratio * len(messages))
    msg_replacements = numpy.random.choice(range(len(messages)), num_replacements)
    for index in msg_replacements:
        new_messages[int(index)].date = random.choice(dates)
    new_messages = set(new_message for new_message in new_messages)
    return new_messages


def clustered_random_dates(past: datetime, cluster_size: int, num_cluster: int, years=1, remainder=0) -> \
        list[datetime]:
    """:param past: the beginning of the time period
    :param num_cluster: the number of clusters in the time period
    :param cluster_size: the size of each cluster of date times
    :param years: the number of years in the time period
    :param remainder: the number of non-clustered date times"""
    dates = list()
    for cluster in range(0, num_cluster):
        date = past + timedelta(days=random.randint(0, years * 365), hours=random.randint(0, 24),
                                minutes=random.randint(0, 60), seconds=random.randint(0, 60))
        for element in range(0, cluster_size):
            dates.append(date + timedelta(minutes=random.randint(0, 59), hours=random.randint(0, 24),
                                          seconds=random.randint(0, 59)))
    dates.extend(date_range(past, numdates=remainder, years=years))
    return dates


def follower_network(followers: list[Account], leaders: list[Account], connectivity=5) -> dict[Account, list[Account]]:
    """:param followers: the accounts of the followers
    :param leaders: the accounts that can be followed
    :param connectivity: the number of people each follower follows"""
    following = dict()
    for i in range(0, len(followers)):
        rand_indices = numpy.random.choice(range(0, len(leaders)), connectivity, replace=False)
        for index in rand_indices:
            if followers[i] in following:
                following[followers[i]].append(leaders[index])
            else:
                following[followers[i]] = [leaders[index]]
    return following


def replace_names(names: list[str], target: list[str]) -> list[str]:
    """:param names: the names being written in
    :param target: the names being written over"""
    new_list = target.copy()
    for i in range(len(target)):
        new_list[i] = names[random.randint(0, len(names) - 1)]
    return new_list


def weight_bag(cluster_size: int, cluster_num, arr: list):
    for cluster in range(0, cluster_size):
        chosen = numpy.random.choice(arr)
        for element in range(0, cluster_num):
            arr.append(chosen)


def store_indices(arr: list, target_value) -> list[int]:
    """returns an array containing all indices in arr containing target_value"""
    indices = []
    for index in range(len(arr)):
        if arr[index] == target_value:
            indices.append(index)
    return indices


def jikeli_date(date_text: str) -> datetime:
    return datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S%z')


def list_to_msg(data: list) -> Message:
    """converts a list of length 4 to a message object; @param data should be in date, text score, username order."""
    msg = Message()
    msg = msg.testing_constructor(data[0], data[1], data[2])
    msg.username = data[3]
    return msg


def replace_keyword(keyword: str, tokens: list[str], replacing_tokens: list[str]) -> list[str]:
    word = lem.lemmatize(keyword.lower())
    new_tokens = list()
    for token in tokens:
        if lem.lemmatize(token.lower()) == word:
            new_tokens.append(numpy.random.choice(replacing_tokens))
        else:
            new_tokens.append(token)
    return new_tokens


def accounts_to_dataframe(accounts: list[Account]) -> pd.DataFrame:
    """saves :param accounts as a dataframe where messages are referenced by ID number only."""
    names = list()
    messages = list()
    subscriptions = list()
    antisemitic = list()
    for account in accounts:
        names.append(str(account.name))
        subscriptions.append([acc.name for acc in account.subscriptions])
        antisemitic.append(account.isAntisemite)
        messages.append(set(int(message.ID) for message in account.messages))
    accounts_df = pd.DataFrame(
        {'Username': names, 'Messages': messages, 'Antisemitic': antisemitic, 'Subscriptions': subscriptions})
    accounts_df.index.name = 'Index'
    return accounts_df


def messages_to_dataframe(messages: set[Message]) -> pd.DataFrame:
    """ Stores @param messages as a dataframe"""
    IDs = list()
    dates = list()
    texts = list()
    scores = list()
    names = list()
    reply_list = list()
    for message in messages:
        IDs.append(message.ID)
        dates.append(message.date.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        texts.append(message.text)
        scores.append(message.score)
        names.append(message.username)
        reply_list.append(message.replying_to)
    df = pd.DataFrame(
        {'Username': names, 'ID': IDs, 'Date': dates, 'Text': texts, 'Score': scores, "Replying_To": reply_list})
    df.index.name = 'Index'
    return df


def assign_messages_randomly(accounts: list[Account], messages: set[Message]) -> None:
    for message in messages:
        user = numpy.random.choice(range(0, len(accounts)))
        accounts[user].messages.add(message)
        message.username = accounts[user].name


def reply_net(messages: set[Message], accounts: list[Account], replies_to_msgs=2) -> None:
    """Modifies a lost of :param messages in place by having them reply to each other,
     with a ratio of :param replies_to_msgs responses per message, with messages from
     :param replies_to_msgs:
     :param messages:
     :param accounts being top level messages."""
    replies_to_msgs = int(replies_to_msgs)
    if replies_to_msgs < 0 or len(messages) / replies_to_msgs <= 1:
        raise ValueError("Must be at least one message to reply to, and positive number of replies.")
    sections = replies_to_msgs + 1
    top_level_messages = list()
    users = dict()
    for account in accounts:
        users[account.name] = account
    rand_indices = numpy.random.choice(range(0, len(messages)), int(len(messages) / sections), replace=False)
    msg_list = list(messages)
    for index in rand_indices:
        if msg_list[index].username in users.keys():
            top_level_messages.append(msg_list[index])
    replies = set(msg_list)
    top_level_set = set(top_level_messages)
    for message in top_level_messages:
        replies.remove(message)
    for message in replies:
        if message.username in users:
            user = users[message.username]
            if numpy.random.choice([True, True, False]) and user.subscriptions:
                subs = user.subscriptions
                rand_sub_num = numpy.random.choice(range(len(subs)), 1, replace=False)
                rand_sub = subs[rand_sub_num[0]]
                sub_messages = list()
                for sub_msg in rand_sub.messages:
                    if sub_msg in top_level_set:
                        sub_messages.append(sub_msg)
                if sub_messages:
                    rand_msg = random.choice(sub_messages)
                    message.replying_to = rand_msg.ID
                    continue
        rand_index = numpy.random.choice(range(len(top_level_messages)))
        chosen_msg = top_level_messages[rand_index]
        message.replying_to = chosen_msg.ID


def parse_single_int(cell: str) -> int:
    """Finds a single integer within a string, ignoring all other characters."""
    word = ""
    for char in cell:
        if char.isdigit():
            word += char
    return int(word)


def parse_list_ints(cell: str) -> set[int]:
    """:returns a list of integers from :param cell, a comma separated list of numbers stored in a string"""
    nums = set()
    num_word = ""
    for char in cell:
        if char.isdigit():
            num_word += char
        if char == ',':
            nums.add(int(num_word))
            num_word = ""
    return nums


def load_accounts() -> set[Account]:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths to the CSV files
    messages_path = os.path.join(script_dir, 'messages.csv')
    accounts_path = os.path.join(script_dir, 'accounts.csv')

    message_data = read_csv(messages_path)
    account_data = read_csv(accounts_path, converters={'Messages': parse_list_ints})

    # Parse message data into a lookup dictionary
    message_lookup = {}
    for _, row in message_data.iterrows():
        msg_list = [datetime.strptime(row['Date'], "%d-%b-%Y (%H:%M:%S.%f)"),
                    row['Text'], row['Score'], row['Username']]
        msg = list_to_msg(msg_list)
        msg.ID = row['ID']
        msg.replying_to = row['Replying_To']
        message_lookup[int(row['ID'])] = msg

    # Initialize Account objects and set feature scores
    accounts = set()
    for _, row in account_data.iterrows():
        messages = {message_lookup[index] for index in row['Messages']}
        antisemitic = row['Antisemitic']
        username = row['Username']
        subscriptions = row['Subscriptions']
        account = Account(name=username, messages=messages, initial_subscriptions=subscriptions,
                          antisemite=antisemitic)
        account.set_feature_scores()
        accounts.add(account)

    return accounts
