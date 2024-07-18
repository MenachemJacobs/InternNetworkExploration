from Components import Account


class StateHolder:
    def __init__(self, all_accounts):
        self.all_accounts = all_accounts
        self.all_accounts = []
        self.overt_accounts = []
        self.counter = 0

    def uncover_overt(self) -> list["Account"]:
        pos_scored_accounts = []

        for account in self.all_accounts:
            if self.test_account(account):
                pos_scored_accounts.append(account)

        return pos_scored_accounts

    def test_account(self, account):
        self.counter += 1

        if self.counter % 5 == 0:
            return True
        else:
            return False
