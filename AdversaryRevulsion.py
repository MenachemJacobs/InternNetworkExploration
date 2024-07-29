from collections import Counter, defaultdict

import nltk.tokenize.casual
from nltk import word_tokenize, ngrams
from nltk.corpus import stopwords
from Components.Account import Account

uninteresting_word_list = {"https", "zionazi", "zionazis", "kikes"}
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
        self.covert_accounts: list[tuple[Account, int]] = []

        self.comparative_hot_words: list[str] = []
        self.absolute_hot_words: list[str] = []

        self.comparative_hot_phrases: list[str] = []
        self.absolute_hot_phrases: list[str] = []

        self.comparative_hot_dates: list[str] = []
        self.absolute_hot_dates: list[str] = []

        self.feature_set: list[list[str]] = []

    def classify(self, all_accounts: set[Account]) -> list[tuple[Account, int]]:
        """
        Classifies accounts by identifying overt accounts, compiling feature sets, and uncovering covert accounts.

        Args:
            all_accounts (set[Account]): set of all Account objects to be analyzed.

        Returns:
            set[Account]: set of covert Account objects identified after classification.
        """
        self.all_accounts: set[Account] = set(account for account in all_accounts)

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

        suspicious_accounts = self.all_accounts - self.overt_accounts

        def count_features(accounts, word_counter, phrase_counter, date_counter):
            for account in accounts:
                for message in account.messages:
                    tokens = [token for token in word_tokenize(message.text.lower())
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

    def uncover_covert(self) -> list[tuple["Account", int]]:
        """
        Identifies covert accounts based on message content and hot word/phrase lists.

        Returns:
            list[tuple[Account, int]]: List of tuples, each containing a covert Account object and its associated score.
        """
        suspicious_accounts = self.all_accounts - self.overt_accounts

        word_set = set(self.absolute_hot_words) | set(self.comparative_hot_words)
        phrase_set = set(self.absolute_hot_phrases) | set(self.comparative_hot_phrases)
        date_set = set(self.absolute_hot_dates) | set(self.comparative_hot_dates)

        accounts_with_score = []

        for account in suspicious_accounts:
            account_score = 0

            for message in account.messages:
                words = [word for word in tokenizer.tokenize(message.text.lower())
                         if word in word_set]

                word_score = sum(word in word_set for word in words)
                phrase_score = sum(f"{words[i]} {words[i + 1]}" in phrase_set for i in range(len(words) - 1))
                date_score = message.date.strftime('%d-%b-%Y') in date_set

                account_score += word_score + phrase_score + date_score

                # TODO replying_to may be an account
                # score for responses
                if any(message.replying_to in a.messages for a in self.overt_accounts):
                    account_score += 1

            accounts_with_score.append((account, account_score))

        # Sort accounts by score in descending order
        accounts_with_score.sort(key=lambda x: x[1], reverse=True)

        # TODO this should be the accounts whose primary scores now top 0.5
        # take only the first 10% of the list
        top_10_percent_index = max(len(accounts_with_score) // 10, 10)
        self.covert_accounts = accounts_with_score[:top_10_percent_index]

        return self.covert_accounts


def investigate_account(listener: CovertLister, account_name: str):
    word_set = set(listener.absolute_hot_words) | set(listener.comparative_hot_words)
    phrase_set = set(listener.absolute_hot_phrases) | set(listener.comparative_hot_phrases)
    date_set = set(listener.absolute_hot_dates) | set(listener.comparative_hot_dates)

    def score_account(account_to_score: Account):
        word_list: defaultdict[str, int] = defaultdict(int)
        phrase_list: defaultdict[str, int] = defaultdict(int)
        date_list: defaultdict[str, int] = defaultdict(int)
        replied_to: defaultdict[Account, int] = defaultdict(int)

        for message in account_to_score.messages:
            words = [word for word in tokenizer.tokenize(message.text.lower()) if word in word_set]

            for word in words:
                word_list[word] += 1

            for phrase in phrase_set:
                phrase_list[phrase] += 1

            for date in date_set:
                date_list[date] += 1

            for a in listener.overt_accounts:
                # Check if the current message is replying to any message from account 'a'
                if message.replying_to in a.messages:
                    replied_to[a] += 1

        return word_list, phrase_list, date_list, replied_to

    for account in listener.all_accounts:
        if account.name == 'yankthatisntbad':
            print()

        if account.name == account_name:
            return score_account(account)

    print("Couldn't find account")
