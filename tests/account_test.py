import unittest
from Components.Account import Account
from Components.Message import Message
from ContextGeneration.GenerateNameNetworks import *
from AdversaryRevulsion import *
from shuffle.create_accounts import accountData
import shuffle.utils


class TestStringMethods(unittest.TestCase):

    def test_uncover(self):
        accounts = list()
        for index in range(len(accountData['Username'])):
            msg_data = accountData['Messages'][index]
            msg_list = [(shuffle.utils.tuple_to_message(data)) for data in msg_data]
            account = Account.Account(accountData['Username'][index], msg_list,
                                      accountData['Subscriptions'][index], accountData['Antisemitic'][index])
            accounts.append(account)
        listener = CovertLister(accounts)
        self.assertTrue(listener.uncover_overt(), "Not detecting overt accounts.")
        self.assertTrue(listener.uncover_covert(), "Returning empty list of covert accounts.")


if __name__ == '__main__':
    unittest.main()
