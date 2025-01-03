import pickle
import unittest
from ContextGeneration.GenerateNameNetworks import *
from AdversaryRevulsion import *
from shuffle import utils


class TestAccountMethods(unittest.TestCase):
    def setUp(self):
        self.accounts = utils.load_accounts()
        self.listener = CovertLister()
        self.listener.all_accounts = self.accounts
        self.clf = pickle.load(open('Components/classifier_scripts/rfc_secondary_classifier.pkl','rb'))

    def test_uncover(self):
        self.assertTrue(self.listener.uncover_overt(), "Not detecting overt accounts.")
        self.assertTrue(self.listener.classify(self.accounts), "Returning empty list of covert accounts.")

    def test_hot_list(self):
        self.listener.uncover_overt()
        hot = self.listener.compile_feature_set()
        self.assertTrue(hot[0], "no absolute hot words identified")
        self.assertTrue(hot[1], "no comparative hot words identified")
        self.assertTrue(hot[2], "no absolute hot phrases identified")
        self.assertTrue(hot[3], "no comparative hot phrases identified")
        self.assertTrue(hot[4], "no absolute hot dates identified")
        self.assertTrue(hot[5], "no comparative hot dates identified")

    def test_account_data(self):
        overt_sum = 0.0
        num_overt = 0
        pro_sum = 0.0
        num_pro = 0
        for account in self.accounts:
            account.set_secondary_score(self.clf)
            if account.isAntisemite:
                num_overt += 1
                overt_sum += account.secondary_score
            else:
                num_pro += 1
                pro_sum += account.secondary_score
        self.assertGreater(overt_sum/num_overt, pro_sum/num_pro, "overt accounts scoring too low on average.")
if __name__ == '__main__':
    unittest.main()
