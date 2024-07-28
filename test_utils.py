import unittest

from shuffle import injectionValues
from shuffle import utils


class TestUtils(unittest.TestCase):
    def test_replace_word(self):
        sent = ["This", "is", "a", "sentence"]
        self.assertNotEqual(sent, utils.replace_words(sent, hotwords.hot_words, 0.5),
                            "Words are not being replaced at all.")

    def test_replace_wrong_ratio(self):
        with self.assertRaises(ValueError):
            utils.replace_words(["some", "words"], hotwords.hot_words, -0.2)

    def test_replace_keyword(self):
        result = utils.replace_keyword("jew", ["jew", "jew", "jew"], ["stuff"])
        self.assertListEqual(result, ["stuff", "stuff", "stuff"], "jew keyword not being replaced.")

    def test_replace_keyword_not_there(self):
        result = utils.replace_keyword("jew", ["This", "is", "a", "sentence"], ["fiddler"])
        self.assertListEqual(result, ["This", "is", "a", "sentence"], "non-key words are being replaced")

    def test_indices(self):
        result = utils.store_indices([1, 0, 1, 1], 1)
        self.assertEqual(result, [0, 2, 3], "indices are not being stored properly.")
