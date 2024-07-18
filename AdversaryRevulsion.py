from collections import Counter

from Components import Account


class CovertLister:
    def __init__(self, all_accounts: list[Account]):
        self.all_accounts: list[Account] = all_accounts
        self.overt_accounts: list[Account] = []
        self.covert_accounts: list[Account] = []

        self.hot_words: list[str] = []
        self.hot_phrases: list[str] = []

        self.counter = 0

    def uncover_overt(self) -> list["Account"]:
        pos_scored_accounts = []

        for account in self.all_accounts:
            if self.test_account(account):
                pos_scored_accounts.append(account)

        self.overt_accounts = pos_scored_accounts
        return self.overt_accounts

    # TODO replace placeholder when true classifier is developed
    def test_account(self, account) -> bool:
        return account.isAntisemite

    # TODO all of this should be replaced with nltk methods for finding the key words and phrases
    def compile_hot_lists(self) -> tuple[list[str], list[str]]:
        word_counter = Counter()
        phrase_counter = Counter()

        for account in self.all_accounts:
            for message in account.messages:
                words = message.text.split()
                word_counter.update(words)

                message_bigrams = [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]
                phrase_counter.update(message_bigrams)

        self.hot_words = [word for word, _ in word_counter.most_common(100)]
        self.hot_phrases = [phrase for phrase, _ in phrase_counter.most_common(100)]

        return self.hot_words, self.hot_phrases

    def uncover_covert(self) -> list[tuple["Account", int]]:
        self.uncover_overt()
        self.compile_hot_lists()

        suspicious_accounts = set(self.all_accounts) - set(self.overt_accounts)
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
    accounts_with_score.sort(key=lambda x: x[1], reverse=True)
    return accounts_with_score
