import numpy.random

from Components.Account import Account
import pandas as pd

from Components.Message import Message


def accounts_to_dataframe(accounts: list[Account]) -> pd.DataFrame:
    names = list()
    messages = list()
    subscriptions = list()
    antisemitic = list()
    for account in accounts:
        names.append(account.name)
        subscriptions.append(account.subscriptions)
        antisemitic.append(account.isAntisemite)
        messages.append([(message.score, message.date, message.text) for message in account.messages])
    accounts_df = pd.DataFrame({ 'Username': names,'Messages': messages, 'Antisemitic': antisemitic,'Subscriptions': subscriptions})
    return accounts_df


def assign_messages_randomly(accounts: list[Account], messages: list[Message]) -> None:
    for message in messages:
        user = numpy.random.choice(range(0, len(accounts)))
        accounts[user].messages.append(message)

