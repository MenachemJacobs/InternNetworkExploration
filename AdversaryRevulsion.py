from collections import Counter

from Components import Account


class CovertLister:
    def __init__(self, all_accounts):
        self.all_accounts = all_accounts
        self.overt_accounts = []
        self.covert_account = []

        self.hot_words = []
        self.hot_phrases = []

        self.counter = 0

    def uncover_overt(self) -> list["Account"]:
        pos_scored_accounts = []

        for account in self.all_accounts:
            if self.test_account(account):
                pos_scored_accounts.append(account)

        self.overt_accounts = pos_scored_accounts

        return self.overt_accounts

    def test_account(self, account) -> bool:
        self.counter += 1

        if self.counter % 5 == 0:
            return True
        else:
            return False

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
        self.hot_phrases = [f"{bigram[0]} {bigram[1]}" for bigram, _ in phrase_counter.most_common(100)]

        return self.hot_words, self.hot_phrases

    def uncover_covert(self) -> list[tuple["Account", int]]:
        suspicious_accounts = self.all_accounts - self.overt_accounts
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

        # sort the list
        account_score_sorter(accounts_with_score)

        # take only the first 10% of the list
        self.covert_account = accounts_with_score[(len(accounts_with_score) // 10):]

        return self.covert_account


def account_score_sorter(accounts_with_score: list[tuple["Account", int]]) -> list[tuple["Account", int]]:
    accounts_with_score.sort(key=lambda x: x[1], reverse=True)
    return accounts_with_score
