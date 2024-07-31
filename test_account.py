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
        self.assertTrue(hot[0], "no hot words identified")
        self.assertTrue(hot[1], "no hot phrases identified")


if __name__ == '__main__':
    unittest.main()
