from collections import Counter

import nltk.tokenize.casual
from nltk import word_tokenize, ngrams
from nltk.corpus import stopwords
from Components.Account import Account

uninteresting_word_list = ["https", "zionazi", "zionazis", "kikes"]


# Filter out common words and phrases
def filter_common(overt_counter, suspicious_counter, num_top):
    """
    Filters out common words and phrases from the top items of overt and suspicious counters.

    Args:
        overt_counter (Counter): Counter object for overt account word/phrase frequencies.
        suspicious_counter (Counter): Counter object for suspicious account word/phrase frequencies.
        num_top (int): Number of top items to consider from the counters.

    Returns:
        list[str]: List of words/phrases that are not common between the overt and suspicious counters.
    """
    common_items = set(dict(overt_counter.most_common(num_top))).intersection(
        set(dict(suspicious_counter.most_common(num_top))))

    # TODO item[0] gets the date, which is all I really want. item[1] is the frequency.
    return [item[0] for item in overt_counter.most_common(num_top) if item[0] not in common_items]


def score_comparatively(overt_counter, suspicious_counter, num_top):
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
        self.covert_accounts: list[Account] = list()
        # pro_accounts = set(all_accounts) - set(overt_accounts) - set(covert_accounts)

        self.comparative_hot_words: list[str] = []
        self.absolute_hot_words: list[str] = []

        self.comparative_hot_phrases: list[str] = []
        self.absolute_hot_phrases: list[str] = []

        self.comparative_hot_dates: list[str] = []
        self.absolute_hot_dates: list[str] = []

        self.negative_feature_set = []

    def classify(self, all_accounts: set[Account]):
        """
        Classifies accounts by identifying overt accounts, compiling feature sets, and uncovering covert accounts.

        Args:
            all_accounts (set[Account]): set of all Account objects to be analyzed.

        Returns:
            set[Account]: set of covert Account objects identified after classification.
        """
        self.all_accounts = all_accounts

        self.uncover_overt()  # Identifies overt accounts
        self.compile_feature_set()  # Compiles feature set
        self.uncover_covert()  # Identifies covert accounts

        return self.covert_accounts

    def uncover_overt(self) -> set["Account"]:
        """
        Identifies overt accounts based on a placeholder classifier.

        Returns:
            set[Account]: Set of overt Account objects.
        """

        # TODO replace placeholder when true classifier is developed
        def test_account(account) -> bool:
            """
            Placeholder method to test if an account is overt.

            Args:
                account (Account): An Account object to be tested.

            Returns:
                bool: True if the account is identified as overt; False otherwise.
            """
            return account.isAntisemite

        self.overt_accounts = set(account for account in self.all_accounts if test_account(account))

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
        overt_word_counter, sus_word_counter = Counter(), Counter()
        overt_phrase_counter, sus_phrase_counter = Counter(), Counter()
        overt_date_counter, sus_date_counter = Counter(), Counter()

        stop_words = set(stopwords.words('english'))
        suspicious_accounts = set(self.all_accounts) - set(self.overt_accounts)

        def process_accounts(accounts, word_counter, phrase_counter, date_counter):
            for account in accounts:
                for message in account.messages:
                    tokens = word_tokenize(message.text.lower())
                    tokens = [token for token in tokens if token.isalnum() and token not in stop_words
                              and token not in uninteresting_word_list]

                    # Update word counter
                    word_counter.update(tokens)

                    # Update phrase counter
                    message_bigrams = list(ngrams(tokens, 2))
                    phrase_counter.update(message_bigrams)

                    # Update date counters
                    date_key = (message.date.strftime('%d-%b-%Y'))
                    date_counter.update([date_key])

        # Process overt accounts
        process_accounts(self.overt_accounts, overt_word_counter, overt_phrase_counter, overt_date_counter)
        # Process suspicious accounts
        process_accounts(suspicious_accounts, sus_word_counter, sus_phrase_counter, sus_date_counter)

        def process_counters(overt_counter, sus_counter, num_top):
            absolute = filter_common(overt_counter, sus_counter, num_top)
            comparative = score_comparatively(overt_counter, sus_counter, num_top)
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

        self.negative_feature_set = [self.absolute_hot_words, self.absolute_hot_phrases, self.absolute_hot_dates,
                                     self.comparative_hot_words, self.comparative_hot_phrases, self.comparative_hot_dates
                                     ]

        return self.negative_feature_set

    def uncover_covert(self) -> list[tuple["Account", int]]:
        """
        Identifies covert accounts based on message content and hot word/phrase lists.

        Returns:
            list[tuple[Account, int]]: List of tuples, each containing a covert Account object and its associated score.
        """
        suspicious_accounts = set(self.all_accounts) - set(self.overt_accounts)
        stop_words = set(stopwords.words('english'))
        tokenizer = nltk.tokenize.casual.TweetTokenizer()
        accounts_with_score = []

        for account in suspicious_accounts:
            account_score = 0

            for message in account.messages:
                words = tokenizer.tokenize(message.text.lower())
                words = [word for word in words if word not in stop_words and word not in uninteresting_word_list]

                # score for words
                for word in words:
                    if word in self.absolute_hot_words or word in self.comparative_hot_words:
                        account_score += 1

                # score for phrase
                for i in range(len(words) - 1):
                    bigram = f"{words[i]} {words[i + 1]}"
                    if bigram in self.absolute_hot_phrases or bigram in self.comparative_hot_phrases:
                        account_score += 1

                # score for date
                if message.date in self.absolute_hot_dates or message.date in self.comparative_hot_dates:
                    account_score += 1

                # TODO replying to may be an account
                # score for responses
                if message.replying_to:
                    for possible_account in self.overt_accounts:
                        if message.replying_to in possible_account.messages:
                            account_score += 1
                            break

            accounts_with_score.append((account, account_score))

        # Sort accounts by score in descending order
        accounts_with_score.sort(key=lambda x: x[1], reverse=True)

        # TODO this should be the accounts whose primary scores now top 0.5
        # take only the first 10% of the list
        top_10_percent_index = max(len(accounts_with_score) // 10, 10)
        self.covert_accounts = accounts_with_score[:top_10_percent_index]

        return self.covert_accounts
