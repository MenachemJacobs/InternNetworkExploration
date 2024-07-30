from pandas import read_csv

from shuffle import injectionValues

from AdversaryRevulsion import CovertLister, investigate_account
from Components.Account import Account

true_covert = set(read_csv('shuffle/covert.csv')['Username'])
true_hot_words = set(word for word in injectionValues.hot_words)
true_hot_phrases = set(phrase for phrase in injectionValues.hot_phrases)


def score_the_features(passed_coverts: set, passed_words: set, passed_phrases: set):
    specious_inclusions = passed_coverts - true_covert
    perfidious_exclusions = true_covert - passed_coverts

    words_wrongly_present = passed_words - true_hot_words
    words_wrongly_not_present = true_hot_phrases - passed_words

    phrases_wrongly_present = passed_phrases - true_hot_phrases
    phrases_wrongly_not_present = true_hot_phrases - passed_phrases

    print("Characters wrongly include:", str(specious_inclusions), "Characters wrongly excluded:",
          str(perfidious_exclusions))
    print("Overall accuracy:", len(specious_inclusions & perfidious_exclusions), "/",
          len(specious_inclusions | perfidious_exclusions))


def score_the_man(lister: CovertLister, account: Account):
    """Pass in an account and a lister to see how the account scores on the lister and in what respects and features"""
    word_list, phrase_list, date_list, replied_to = investigate_account(lister, account.name)
    list_list = [word_list, phrase_list, date_list, replied_to]
    print(account)
    for sub_list in list_list:
        print(sub_list)
