from collections import Counter, defaultdict

import nltk.tokenize.casual
from nltk import ngrams
from nltk.corpus import stopwords
from Components.Account import Account

uninteresting_word_list = {}
tokenizer = nltk.tokenize.casual.TweetTokenizer()
stop_words = set(stopwords.words('english'))

overt_word_counter, sus_word_counter = Counter(), Counter()
overt_phrase_counter, sus_phrase_counter = Counter(), Counter()
overt_date_counter, sus_date_counter = Counter(), Counter()


# Filter out common words and phrases
def filter_common(overt_counter, suspicious_counter, num_top) -> list:
    """
    Filters out common words and phrases from the top items of overt and suspicious counters.

    Args:
        overt_counter (Counter): Counter object for overt account word/phrase frequencies.
        suspicious_counter (Counter): Counter object for suspicious account word/phrase frequencies.
        num_top (int): Number of top items to consider from the counters.

    Returns:
        list[str]: List of words/phrases that are not common between the overt and suspicious counters.
    """
    common_items = set(overt_counter.most_common(num_top)) & set(suspicious_counter.most_common(100))

    # TODO item[0] gets the date, which is all I really want. item[1] is the frequency.
    return [item[0] for item in overt_counter.most_common(num_top) if item[0] not in common_items]


def score_comparatively(overt_counter, suspicious_counter, num_top) -> list:
    """
    Computes a comparative score between overt and suspicious counters.

    Args:
        overt_counter (Counter): Counter object for overt account word/phrase frequencies.
        suspicious_counter (Counter): Counter object for suspicious account word/phrase frequencies.
        num_top (int): Number of top items to consider from the counters.

    Returns:
        list[tuple[str, float]]: List of top comparative scores with their corresponding items.
    """
    # Normalize overt_counter and suspicious_counter
    overt_normalized = Counter({k: v / len(overt_counter) for k, v in overt_counter.items()})
    sus_normalized = Counter({k: v / len(suspicious_counter) for k, v in suspicious_counter.items()})

    # Compute the comparative score and then rescale
    comparative_counter = overt_normalized - sus_normalized
    comparative_counter = Counter({k: v * len(overt_normalized) for k, v in comparative_counter.items()})

    return [item[0] for item in comparative_counter.most_common(num_top)]


class CovertLister:
    """
    Class for analyzing a list of Account objects to identify overt and covert accounts based on message content.

    Attributes: all_accounts (list[Account]): List of all Account objects provided for analysis. overt_accounts (
    list[Account]): List of accounts identified as overt. covert_accounts (list[tuple[Account, int]]): List of
    tuples, each containing a covert Account object and its associated score. absolute_hot_words (list[str]): List of
    frequently occurring individual words across all messages. absolute_hot_phrases (list[str]): List of frequently
    occurring phrases (bigrams) across all messages. absolute_hot_dates (list[str]): List of frequently occurring
    dates across all messages. comparative_hot_words (list[str]): List of comparatively significant words across
    messages. comparative_hot_phrases (list[str]): List of comparatively significant phrases (bigrams) across
    messages. comparative_hot_dates (list[str]): List of comparatively significant dates across messages.
    negative_feature_set (list[list]): Aggregated list of all feature sets for analysis.

    Methods:
        __init__(self):
            Initializes a CovertLister object with empty attributes.

        classify(self, all_accounts: list[Account]) -> list[Account]:
            Identifies overt accounts, compiles feature sets, and uncovers covert accounts.

        uncover_overt(self) -> list[Account]:
            Identifies overt accounts based on a placeholder classifier.

        compile_feature_set(self) -> list[list]: Generates and returns lists of frequently occurring words, phrases,
        and dates, both absolutely and comparatively.

        uncover_covert(self) -> list[tuple[Account, int]]:
            Identifies covert accounts based on message content and hot word/phrase lists.

        account_score_sorter(accounts_with_score: list[tuple[Account, int]]) -> list[tuple[Account, int]]:
            Sorts a list of tuples based on the score in descending order.
    """

    def __init__(self):
        """
        Initializes a CovertLister object with empty lists or counters for attributes.
        """
        self.all_accounts: set[Account] = set()
        self.overt_accounts: set[Account] = set()
        # self.covert_accounts: list[tuple[Account, int]] = []

        self.comparative_hot_words: list[str] = []
        self.absolute_hot_words: list[str] = []

        self.comparative_hot_phrases: list[str] = []
        self.absolute_hot_phrases: list[str] = []

        self.comparative_hot_dates: list[str] = []
        self.absolute_hot_dates: list[str] = []

        # TODO relative and absolute dates

        self.feature_set: list[list[str]] = []

    def classify(self, all_accounts: set[Account]) -> list[list[str]]:
        """
        Classifies accounts by identifying overt accounts, compiling feature sets, and uncovering covert accounts.

        Args:
            all_accounts (set[Account]): set of all Account objects to be analyzed.

        Returns:
            list[list]: the feature set containing all the scored features.
        """
        self.all_accounts: set[Account] = set(account for account in all_accounts)

        self.uncover_overt()  # Identifies overt accounts
        self.compile_feature_set()  # Compiles feature set

        return self.feature_set

    def uncover_overt(self) -> set["Account"]:
        """
        Identifies overt accounts based on a placeholder classifier.

        Returns:
            set[Account]: Set of overt Account objects.
        """

        self.overt_accounts = set(account for account in self.all_accounts if account.primary_score > 0.5)

        return self.overt_accounts

    def compile_feature_set(self) -> list[list]:
        """
        Compiles lists of frequently occurring words, phrases, and dates across all messages from overt and
        suspicious accounts.

        Returns:
            list[list]: Aggregated list containing:
                - absolute_hot_words (list[str]): Top 100 most frequent words.
                - comparative_hot_words (list[str]): Top 100 most comparative significant words.
                - absolute_hot_phrases (list[str]): Top 100 most frequent phrases (bigrams).
                - comparative_hot_phrases (list[str]): Top 100 most comparative significant phrases (bigrams).
                - absolute_hot_dates (list[str]): Top 100 most frequent dates.
                - comparative_hot_dates (list[str]): Top 100 most comparative significant dates.
        """

        suspicious_accounts = self.all_accounts - self.overt_accounts

        def count_features(accounts, word_counter, phrase_counter, date_counter):
            for account in accounts:
                for message in account.messages:
                    tokens = [token for token in tokenizer.tokenize(message.text.lower())
                              if token.isalnum() and token not in stop_words and token not in uninteresting_word_list]

                    # Update word counter
                    word_counter.update(tokens)

                    # Update phrase counter. It is possible the assignment should use a list.
                    message_bigrams = ngrams(tokens, 2)
                    phrase_counter.update(message_bigrams)

                    # Update date counters
                    date_key = (message.date.strftime('%d-%b-%Y'))
                    date_counter.update([date_key])

        # Process overt accounts
        count_features(self.overt_accounts, overt_word_counter, overt_phrase_counter, overt_date_counter)
        # Process suspicious accounts
        count_features(suspicious_accounts, sus_word_counter, sus_phrase_counter, sus_date_counter)

        def process_counters(overt_counter, sus_counter, num_top) -> tuple[list, list]:
            absolute: list = filter_common(overt_counter, sus_counter, num_top)
            comparative: list = score_comparatively(overt_counter, sus_counter, num_top)
            return absolute, comparative

        # Process word counters
        self.absolute_hot_words, self.comparative_hot_words = (
            process_counters(overt_word_counter, sus_word_counter, 100))

        # Process phrase counters
        self.absolute_hot_phrases, self.comparative_hot_phrases = (
            process_counters(overt_phrase_counter, sus_phrase_counter, 100))

        # Process date counters
        self.absolute_hot_dates, self.comparative_hot_dates = (
            process_counters(overt_date_counter, sus_date_counter, 100))

        self.feature_set = [self.absolute_hot_words, self.comparative_hot_words, self.absolute_hot_phrases,
                            self.comparative_hot_phrases, self.absolute_hot_dates, self.comparative_hot_dates]

        return self.feature_set


def investigate_account(listener: CovertLister, account_name: str) -> list[float]:
    """return the feature set scores for an individual account. Scores require the system already be trained on overt
    accounts

    :return: a list of seven integer values, corresponding to the feature set scores"""

    def score_account(account_to_score: Account) -> list[float]:
        features_dictionaries: defaultdict[str, float] = defaultdict(float)

        feature_keys = ["absolute_hot_words", "comparative_hot_words", "absolute_hot_phrases",
                        "comparative_hot_phrases", "absolute_hot_dates", "comparative_hot_dates",
                        "replying_to"]

        for key in feature_keys:
            features_dictionaries[key] = 0

        for message in account_to_score.messages:
            words = [word for word in tokenizer.tokenize(message.text.lower())
                     if word.isalnum() and word not in stop_words and word not in uninteresting_word_list]

            for i in range(len(words)):
                word = words[i]

                if word in listener.absolute_hot_words:
                    features_dictionaries[feature_keys[0]] += 1
                if word in listener.comparative_hot_words:
                    features_dictionaries[feature_keys[1]] += 1

                if i < len(words) - 1:
                    phrase = (words[i], words[i + 1])
                    if phrase in listener.absolute_hot_phrases:
                        features_dictionaries[feature_keys[2]] += 1
                    if phrase in listener.comparative_hot_phrases:
                        features_dictionaries[feature_keys[3]] += 1

            formatted_date = str(message.date.strftime('%d-%b-%Y'))
            if formatted_date in listener.absolute_hot_dates:
                features_dictionaries[feature_keys[4]] += 1
            if formatted_date in listener.comparative_hot_dates:
                features_dictionaries[feature_keys[5]] += 1

            if message.replying_to:
                for overt in listener.overt_accounts:
                    message_ids = set(message.ID for message in overt.messages)
                    if message.replying_to in message_ids:
                        features_dictionaries[feature_keys[6]] += 1

        values = [features_dictionaries[key] for key in feature_keys]
        return values

    for account in listener.all_accounts:
        if account.name == account_name:
            return score_account(account)

    print("Couldn't find account", account_name)
    return [0] * 7  # Return a default value in case account is not found
