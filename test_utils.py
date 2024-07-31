import random
import unittest

from shuffle import injectionValues
from shuffle import utils


class TestUtils(unittest.TestCase):

    def test_replace_word(self):
        sent = ["This", "is", "a", "sentence"]
        self.assertNotEqual(sent, utils.replace_words(sent, injectionValues.hot_words, 0.5),
                            "Words are not being replaced at all.")

    def test_replace_wrong_ratio(self):
        with self.assertRaises(ValueError):
            utils.replace_words(["some", "words"], injectionValues.hot_words, -0.2)

    def test_replace_keyword(self):
        result = utils.replace_keyword("jew", ["jew", "jew", "jew"], ["stuff"])
        self.assertListEqual(result, ["stuff", "stuff", "stuff"], "jew keyword not being replaced.")

    def test_replace_keyword_not_there(self):
        result = utils.replace_keyword("jew", ["This", "is", "a", "sentence"], ["fiddler"])
        self.assertListEqual(result, ["This", "is", "a", "sentence"], "non-key words are being replaced")

    def test_indices(self):
        result = utils.store_indices([1, 0, 1, 1], 1)
        self.assertEqual(result, [0, 2, 3], "indices are not being stored properly.")

    def test_load_accounts(self):
        accounts = utils.load_accounts()
        account = random.choice(list(accounts))
        self.assertTrue(account.subscriptions, "account has not subscriptions")
        self.assertTrue(account.messages, "account has no messages")
        features = account.feature_list.copy()
        account.set_feature_scores()
        self.assertEqual(account.feature_list, features, "feature list not set by load_accounts.")
