from datetime import timedelta

import Classifier
from Message import Message


class Account:
    def __init__(self, name: str, messages: ['Message'] = None, initial_subscriptions: ['Account'] = None):
        self.name = name

        self.messages = messages
        self.subscriptions = initial_subscriptions

        """Feature list"""
        self.score_per_day = self.set_score_per_day()
        self.score_by_density = 1.0
        self.positives_per_tweet = 1.0

        self.feature_list = [
            self.score_per_day, self.score_by_density, self.positives_per_tweet
        ]

        self.secondary_score = 1.0
        self.primary_score = 1.0

    """Averaging will only work when both the numerator (the number of messages), and the denominator are non-zero. 
    This requires the account to be at least one day old."""
    def set_score_per_day(self):
        span = max(self.messages, key=lambda m: m.date).date - min(self.messages, key=lambda m: m.date).date
        return sum(message.score for message in self.messages) / span.days

    def set_score_by_density(self):
        partitions = 100

        # Get the date range
        first_day = min(self.messages, key=lambda m: m.date).date
        last_day = max(self.messages, key=lambda m: m.date).date
        total_days = (last_day - first_day).days
        period_length = timedelta(days = total_days / partitions)

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

    def set_secondary_score(self):
        self.secondary_score = Classifier.calculate_secondary_score(self.feature_list)

    def set_primary_score(self):
        self.primary_score = 0

        if self.secondary_score == 1.0:
            self.set_secondary_score()

        for subscriber in self.subscriptions:
            if subscriber.secondary_score == 1.0:
                subscriber.set_secondary_score()
            self.primary_score += subscriber.secondary_score

        """Weight the secondary score of this account twice as heavily as the score from the subscriptions"""
        self.primary_score += 2 * self.secondary_score
        self.primary_score /= len(self.feature_list) + 2

    def add_subscriber(self, subscriber: 'Account'):
        if isinstance(subscriber, Account) and subscriber not in self.subscriptions:
            self.subscriptions.append(subscriber)

    def add_subscribers(self, neighbors):
        for subscriber in neighbors:
            self.add_subscriber(subscriber)

    # def add_superscriber(self, superscriber: 'Account'):
    #     if isinstance(superscriber, Account) and superscriber not in self.subscribers:
    #         self.superscribers.append(superscriber)

    def remove_subscriber(self, neighbor: 'Account'):
        if neighbor in self.subscriptions:
            self.subscriptions.remove(neighbor)
            return True
        else:
            return False

    def get_subscribers(self):
        return self.subscriptions

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()