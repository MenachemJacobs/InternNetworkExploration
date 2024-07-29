import unittest
from ContextGeneration.GenerateNameNetworks import *
from AdversaryRevulsion import *
from App import accountData, messageLookup


class TestAccountMethods(unittest.TestCase):
    def setUp(self):
        self.accounts = set()
        for index in range(len(accountData['Username'])):
            msg_indexes = accountData['Messages'][index]
            msg_list = set()
            for indice in msg_indexes:
                msg_list.add(messageLookup[indice])
            account = Account(accountData['Username'][index], msg_list, accountData['Subscriptions'][index],
                              accountData['Antisemitic'][index])
            self.accounts.add(account)
        self.listener = CovertLister()
        self.listener.all_accounts = self.accounts

    def test_uncover(self):
        self.assertTrue(self.listener.uncover_overt(), "Not detecting overt accounts.")
        self.assertTrue(self.listener.uncover_covert(), "Returning empty list of covert accounts.")

    def test_hot_list(self):
        self.listener.uncover_overt()

        hot = self.listener.compile_feature_set()
        self.assertTrue(hot[0], "no hot words identified")
        self.assertTrue(hot[1], "no hot phrases identified")


if __name__ == '__main__':
    unittest.main()
