from collections import Counter

from Components import Account

from nltk.corpus import stopwords


class CovertLister:
    """
    Class for analyzing a list of Account objects to identify overt and covert accounts based on message content.

    Attributes:
        all_accounts (list[Account]): List of all Account objects provided for analysis.
        overt_accounts (list[Account]): List of accounts identified as overt.
        covert_accounts (list[Account]): List of accounts identified as covert.
        hot_words (list[str]): List of frequently occurring individual words across all messages.
        hot_phrases (list[str]): List of frequently occurring phrases (bigrams) across all messages.
        counter (int): Internal counter, initialized to 0.

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

        self.counter = 0

    def uncover_overt(self) -> list["Account"]:
        """
        Identifies overt accounts based on a placeholder classifier (test_account method).

        Returns:
            list[Account]: List of overt Account objects.
        """
        pos_scored_accounts = []

        for account in self.all_accounts:
            if self.test_account(account):
                pos_scored_accounts.append(account)

        self.overt_accounts = pos_scored_accounts
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
    def compile_hot_lists(self, suspicious_accounts: list["Account"]) -> tuple[list[str], list[str]]:
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

        # find most most common words and phrases in overt list
        for account in self.overt_accounts:
            for message in account.messages:
                anti_words = message.text.split()
                anti_words = [word for word in anti_words if word.lower() not in stop_words]
                overt_word_counter.update(anti_words)

                message_bigrams = [f"{anti_words[i]} {anti_words[i + 1]}" for i in range(len(anti_words) - 1)]
                overt_phrase_counter.update(message_bigrams)

        # find most most common words and phrases in suspicious list
        for account in suspicious_accounts:
            for message in account.messages:
                pro_words = message.text.split()
                pro_words = [word for word in pro_words if word.lower() not in stop_words]
                sus_word_counter.update(pro_words)

                message_bigrams = [f"{pro_words[i]} {pro_words[i + 1]}" for i in range(len(pro_words) - 1)]
                sus_phrase_counter.update(message_bigrams)


        # filter out word that apear in both lists
        self.hot_words = [word for word, _ in overt_word_counter.most_common(100) if word not in sus_word_counter.most_common(100)]
        self.hot_phrases = [phrase for phrase, _ in overt_phrase_counter.most_common(100)if phrase not in sus_phrase_counter.most_common(100)]

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

        # sort the list in place
        account_score_sorter(accounts_with_score)

        # take only the first 10% of the list
        top_10_percent_index = len(accounts_with_score) // 10
        self.covert_accounts = accounts_with_score[:top_10_percent_index]

        return self.covert_accounts


def account_score_sorter(accounts_with_score: list[tuple["Account", int]]) -> list[tuple["Account", int]]:
    """
    Sorts a list of tuples based on the score in descending order.

    Args:
        accounts_with_score (list[tuple[Account, int]]): List of tuples containing Account objects and scores.

    Returns:
        list[tuple[Account, int]]: Sorted list of tuples in descending order of scores.
    """
    accounts_with_score.sort(key=lambda x: x[1], reverse=True)
    return accounts_with_score
