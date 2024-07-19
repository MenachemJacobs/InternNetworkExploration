from collections import Counter
from nltk import word_tokenize, ngrams
from nltk.corpus import stopwords
from Components import Account


class CovertLister:
    """
    Class for analyzing a list of Account objects to identify overt and covert accounts based on message content.

    Attributes:
        all_accounts (list[Account]): List of all Account objects provided for analysis.
        overt_accounts (list[Account]): List of accounts identified as overt.
        covert_accounts (list[Account]): List of accounts identified as covert.
        hot_words (list[str]): List of frequently occurring individual words across all messages.
        hot_phrases (list[str]): List of frequently occurring phrases (bigrams) across all messages.

    Methods:
        __init__(self, all_accounts: list[Account]):
            Initializes a CovertLister object with a list of Account objects.

        uncover_overt(self) -> list[Account]:
            Identifies overt accounts based on a placeholder classifier (test_account method).

        test_account(self, account) -> bool:
            Placeholder method to test if an account is overt.

        compile_hot_lists(self) -> tuple[list[str], list[str]]:
            Generates lists of frequently occurring words and phrases across all messages.

        uncover_covert(self) -> list[tuple[Account, int]]:
            Identifies covert accounts based on message content and hot word/phrase lists.

        account_score_sorter(accounts_with_score: list[tuple[Account, int]]) -> list[tuple[Account, int]]:
            Sorts a list of tuples based on the score in descending order.
    """

    def __init__(self):
        """
        Initializes a CovertLister object.

        Attributes are initialized as empty lists or counters.
        """
        self.all_accounts: list[Account] = []
        self.overt_accounts: list[Account] = []
        self.covert_accounts: list[Account] = []

        self.hot_words: list[str] = []
        self.hot_phrases: list[str] = []

    def uncover_overt(self) -> list["Account"]:
        """
        Identifies overt accounts based on a placeholder classifier (test_account method).

        Returns:
            list[Account]: List of overt Account objects.
        """
        for account in self.all_accounts:
            if self.test_account(account):
                self.overt_accounts.append(account)

        return self.overt_accounts

    # TODO replace placeholder when true classifier is developed
    def test_account(self, account) -> bool:
        """
        Placeholder method to test if an account is overt.

        Args:
            account: An Account object to be tested.

        Returns:
            bool: True if the account is identified as overt; False otherwise.
        """
        return account.isAntisemite

    # TODO all of this should be replaced with nltk methods for finding the key words and phrases
    def compile_hot_lists(self, suspicious_accounts):
        """
        Generates lists of frequently occurring words and phrases across all messages.

        Returns:
            tuple[list[str], list[str]]: A tuple containing:
                - hot_words (list[str]): Top 100 most frequent words.
                - hot_phrases (list[str]): Top 100 most frequent phrases (bigrams).
        """
        overt_word_counter = Counter()
        overt_phrase_counter = Counter()
        sus_word_counter = Counter()
        sus_phrase_counter = Counter()

        stop_words = set(stopwords.words('english'))

        def process_messages(accounts, word_counter, phrase_counter):
            for account in accounts:
                for message in account.messages:
                    tokens = word_tokenize(message.text.lower())
                    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]

                    # Update word counter
                    word_counter.update(tokens)

                    # Update phrase counter
                    message_bigrams = list(ngrams(tokens, 2))
                    phrase_counter.update(message_bigrams)

        # Process overt accounts
        process_messages(self.overt_accounts, overt_word_counter, overt_phrase_counter)

        # Process suspicious accounts
        process_messages(suspicious_accounts, sus_word_counter, sus_phrase_counter)

        # Filter out common words and phrases
        def filter_common(counter1, counter2, num_top):
            common_items = set(dict(counter1.most_common(num_top))).intersection(
                set(dict(counter2.most_common(num_top))))
            return [item for item in counter1.keys() if item not in common_items][:num_top]

        self.hot_words = filter_common(overt_word_counter, sus_word_counter, 100)
        self.hot_phrases = filter_common(overt_phrase_counter, sus_phrase_counter, 100)

        # self.hot_words = overt_word_counter.most_common(100)
        # self.hot_phrases = overt_phrase_counter.most_common(100)

        return self.hot_words, self.hot_phrases

    def uncover_covert(self, all_accounts: list[Account]) -> list[tuple["Account", int]]:
        """
        Identifies covert accounts based on message content and hot word/phrase lists.

        Args:
            all_accounts (list[Account]): List of all Account objects to be analyzed.

        Returns:
            list[tuple[Account, int]]: List of tuples, each containing an Account object and its associated score.
        """
        self.all_accounts = all_accounts
        self.uncover_overt()
        print(self.overt_accounts)
        suspicious_accounts = set(self.all_accounts) - set(self.overt_accounts)

        self.compile_hot_lists(suspicious_accounts)

        accounts_with_score = []

        for account in suspicious_accounts:
            account_score = 0

            for message in account.messages:
                words = message.text.split()

                for word in words:
                    if word in self.hot_words:
                        account_score += 1

                for i in range(len(words) - 1):
                    bigram = f"{words[i]} {words[i + 1]}"
                    if bigram in self.hot_phrases:
                        account_score += 1

            accounts_with_score.append((account, account_score))

        # Sort accounts by score in descending order
        accounts_with_score.sort(key=lambda x: x[1], reverse=True)

        # take only the first 10% of the list
        top_10_percent_index = len(accounts_with_score) // 10
        self.covert_accounts = accounts_with_score[:top_10_percent_index]

        return self.covert_accounts
