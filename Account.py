import Classifier


class Account:
    def __init__(self, name: str):
        self.name = name

        self.primary_score = 1.0
        self.secondary_score = 1.0

        """Feature list"""
        self.score_per_year = 1.0
        self.score_by_density = 1.0
        self.positives_per_tweet = 1.0

        self.feature_list = [
            self.score_per_year, self.score_by_density, self.positives_per_tweet
        ]

        self.messages = []
        self.subscribers = []
        # self.superscribers = []

    def set_secondary_score(self):
        self.secondary_score = Classifier.calculate_secondary_score(self.feature_list)

    def set_primary_score(self):
        self.primary_score = 0

        if self.secondary_score == 1.0:
            self.set_secondary_score()

        for subscriber in self.subscribers:
            if subscriber.secondary_score == 1.0:
                subscriber.set_secondary_score()
            self.primary_score += subscriber.secondary_score

        """Weight the secondary score of this account twice as heavily as the score from the subscriptions"""
        self.primary_score += 2 * self.secondary_score
        self.primary_score /= len(self.feature_list) + 2

    def add_subscriber(self, subscriber: 'Account'):
        if isinstance(subscriber, Account) and subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def add_subscribers(self, neighbors):
        for subscriber in neighbors:
            self.add_subscriber(subscriber)

    # def add_superscriber(self, superscriber: 'Account'):
    #     if isinstance(superscriber, Account) and superscriber not in self.subscribers:
    #         self.superscribers.append(superscriber)

    def remove_subscriber(self, neighbor: 'Account'):
        if neighbor in self.subscribers:
            self.subscribers.remove(neighbor)
            return True
        else:
            return False

    def get_subscribers(self):
        return self.subscribers

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()