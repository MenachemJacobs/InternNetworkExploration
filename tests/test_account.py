import unittest
from Components.Account import Account
from Components.Message import Message
from ContextGeneration.GenerateNameNetworks import *
from AdversaryRevulsion import *
from shuffle.create_accounts import accountData
import shuffle.utils


class TestAccountMethods(unittest.TestCase):
    def setUp(self):
        self.accounts = list()
        for index in range(len(accountData['Username'])):
            msg_data = accountData['Messages'][index]
            msg_list = [(shuffle.utils.list_to_msg(data)) for data in msg_data]
            account = Account.Account(accountData['Username'][index], msg_list,
                                      accountData['Subscriptions'][index], accountData['Antisemitic'][index])
            self.accounts.append(account)
        self.listener = CovertLister()
        self.listener.all_accounts = self.accounts

    def test_uncover(self):
        self.assertTrue(self.listener.uncover_overt(), "Not detecting overt accounts.")
        self.assertTrue(self.listener.uncover_covert(self.accounts), "Returning empty list of covert accounts.")

    def test_hotlist(self):
        suspects = [account[0] for account in self.listener.uncover_covert(all_accounts=self.accounts)]
        self.listener.uncover_overt()
        self.listener.compile_hot_lists(suspects)
        self.assertTrue(self.listener.hot_phrases, "no hot phrases identified")
        self.assertTrue(self.listener.hot_words, "no hot words identified")


if __name__ == '__main__':
    unittest.main()
