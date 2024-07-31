import unittest
from ContextGeneration.GenerateNameNetworks import *
from AdversaryRevulsion import *
from shuffle import utils


class TestAccountMethods(unittest.TestCase):
    def setUp(self):
        self.accounts = utils.load_accounts()
        self.listener = CovertLister()
        self.listener.all_accounts = self.accounts

    def test_uncover(self):
        self.assertTrue(self.listener.uncover_overt(), "Not detecting overt accounts.")
        self.assertTrue(self.listener.uncover_covert(), "Returning empty list of covert accounts.")

    def test_hot_list(self):
        self.listener.uncover_overt()
        hot = self.listener.compile_feature_set()
        self.assertTrue(hot[0], "no absolute hot words identified")
        self.assertTrue(hot[1], "no comparative hot words identified")
        self.assertTrue(hot[2], "no absolute hot phrases identified")
        self.assertTrue(hot[3], "no comparative hot phrases identified")
        self.assertTrue(hot[4], "no absolute hot dates identified")
        self.assertTrue(hot[5], "no comparative hot dates identified")

    def test_load_accounts(self):
        account = random.choice(list(self.accounts))
        self.assertTrue(account.subscriptions, "account has not subscriptions")
        self.assertTrue(account.messages, "account has no messages")
        features = account.feature_list.copy()
        account.set_feature_scores()
        self.assertEqual(account.feature_list, features, "feature list not set by load_accounts.")

    def test_account_data(self):
        overt_sum = 0.0
        num_overt = 0
        pro_sum = 0.0
        num_pro = 0
        for account in self.accounts:
            account.set_secondary_score()
            if account.isAntisemite:
                num_overt += 1
                overt_sum += account.secondary_score
            else:
                num_pro += 1
                pro_sum += account.secondary_score
        self.assertGreater(overt_sum/num_overt, pro_sum/num_pro, "overt accounts scoring too low on average.")
if __name__ == '__main__':
    unittest.main()
