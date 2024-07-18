from datetime import timedelta
from Components import Classifier
from Components.Message import random_message, Message


def random_account(name) -> "Account":
    """
    Create a random Account with the specified name.

    Args:
        name (str): The name of the account.

    Returns:
        Account: An Account object with random messages.
    """
    return Account(name, random_message(5), [])


def create_accounts_by_bulk(names) -> list["Account"]:
    """
    Create multiple accounts by bulk with given names.

    Args:
        names (list[str]): A list of names for the accounts.

    Returns:
        list[Account]: A list of Account objects.
    """
    return [random_account(name) for name in names]


class Account:
    def __init__(self, name: str, messages: list['Message'], initial_subscriptions: list['Account'], antisemite=False):
        """
        Initialize an Account.

        Args:
            name (str): The name of the account.
            messages (list[Message]): A list of Message objects.
            initial_subscriptions (list[Account]): A list of initial subscriptions (Account objects).
            antisemite (bool, optional): Indicates if the account is antisemitic. Defaults to False.
        """
        self.isAntisemite = antisemite
        self.name = name

        self.messages = messages
        self.subscriptions = initial_subscriptions

        """Feature list"""
        self.average_message_score = None
        self.score_per_day = None
        self.score_by_density = None
        self.positives_per_tweet = None

        self.feature_list = []

        self.secondary_score = 1.0
        self.primary_score = 1.0

    def set_feature_scores(self) -> None:
        """
        Calculate and set the feature scores for the account.
        """
        self.average_message_score = sum(m.score for m in self.messages) / len(self.messages)
        self.score_per_day = self.calculate_score_per_day()
        self.score_by_density = self.calculate_score_by_density()
        self.positives_per_tweet = len([m for m in self.messages if m.score > 0.5]) / len(self.messages)

        self.feature_list = [
            self.average_message_score, self.score_per_day, self.score_by_density, self.positives_per_tweet
        ]

    """Averaging will only work when both the numerator (the number of messages), and the denominator are non-zero. 
    This requires the account to be at least one day old."""
    def calculate_score_per_day(self):
        """
        Calculate the average score per day for the account.

        Returns:
            float: The average score per day.
        """

        span = max(self.messages, key=lambda m: m.date).date - min(self.messages, key=lambda m: m.date).date
        return sum(message.score for message in self.messages) / span.days

    """Each tweet's score is multiplied by the number of tweet's in a given period. This weighted average is then
    normalized."""
    def calculate_score_by_density(self):
        """
        Calculate the weighted by post density for the account.

        Returns:
            float: The density-based score.
        """
        partitions = 100

        # Get the date range
        first_day = min(self.messages, key=lambda m: m.date).date
        last_day = max(self.messages, key=lambda m: m.date).date
        total_days = (last_day - first_day).days
        period_length = timedelta(days=total_days / partitions)

        final_score = 0

        current_period = first_day

        for _ in range(partitions):
            period_compound_score = 0
            period_messages = [m for m in self.messages if current_period <= m.date < current_period + period_length]

            if period_messages:
                # Calculate sum of scores and number of messages in this period
                period_score_sum = sum(m.score for m in period_messages)
                period_num_messages = len(period_messages)
                # Calculate the compound score for this period
                period_compound_score = period_score_sum * period_num_messages

            # Move to the next period
            current_period += period_length
            # Add the period's compound score to the final score
            final_score += period_compound_score

        # Normalize the final score by the total number of messages
        return final_score / len(self.messages)

    # return self is necessary for chaining. It is expedient, but perhaps lazy
    def set_secondary_score(self):
        """
        Set the secondary score for the account.

        Returns:
            Account: The current Account object.
        """
        self.secondary_score = Classifier.calculate_secondary_score(self.feature_list)
        return self

    def set_primary_score(self):
        """
        Calculate and set the primary score for the account.
        """
        collated_score = 0

        if self.secondary_score == 1.0:
            self.set_secondary_score()

        for subscriber in self.subscriptions:
            if subscriber.secondary_score == 1.0:
                subscriber.set_secondary_score()
            collated_score += subscriber.secondary_score

        """Weight the secondary score of this account twice as heavily as the score from the subscriptions"""
        collated_score /= len(self.subscriptions)
        self.primary_score = (self.secondary_score + collated_score) / 2

    def add_subscription(self, subscriber: 'Account'):
        """
        Add a subscription to the account.

        Args:
            subscriber (Account): The account to subscribe to.
        """
        if isinstance(subscriber, Account) and subscriber not in self.subscriptions:
            self.subscriptions.append(subscriber)

    def add_subscriptions(self, neighbors):
        """
        Add multiple subscriptions to the account.

        Args:
            neighbors (list[Account]): A list of accounts to subscribe to.
        """
        [self.add_subscription(subscriber) for subscriber in neighbors]

    # def add_super-scriber(self, super-scriber: 'Account'):
    #     if isinstance(super-scriber, Account) and super-scriber not in self.subscribers:
    #         self.super-scribers.append(super-scriber)

    def remove_subscription(self, neighbor: 'Account'):
        """
        Remove a subscription from the account.

        Args:
            neighbor (Account): The account to unsubscribe from.

        Returns:
            bool: True if the subscription was removed, False otherwise.
        """
        if neighbor in self.subscriptions:
            self.subscriptions.remove(neighbor)
            return True
        else:
            return False

    def get_subscriptions(self):
        """
        Get the list of subscriptions for the account.

        Returns:
            list[Account]: A list of accounts this account is subscribed to.
        """
        return self.subscriptions

    def __str__(self):
        """
        String representation of the account.

        Returns:
            str: The account name.
        """
        return "Account: " + self.name

    def __repr__(self):
        """
        Representation of the account.

        Returns:
            str: The account name.
        """
        return self.__str__()