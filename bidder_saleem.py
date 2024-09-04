"""Bidder Class"""
import numpy as np
class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    def __init__(self, num_users, num_rounds):
        '''Setting initial balance to 0, number of users, number of rounds, and round counter'''
        self.balance = 0
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.round_count = 0
        self.user_prob = {}  # build a user_prob based on winnings
        self.winning_bids = []  # Keep track of the winning bids
        self.current_user_id = None #Keep track of the last user_id
        self.epsilon = 1.0 # Initial exploration rate
        self.decay_rate = 0.01  # Rate at which epsilon decays

    def __repr__(self):
        '''Return Bidder object with balance'''
        return self.__str__()

    def __str__(self):
        '''Return Bidder object with balance'''
        return f"Bidder(num_users={self.num_users}, num_rounds={self.num_rounds}), {self.balance})"

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''

        self.current_user_id = user_id  # Update the current user id
        #Initialize probability
        if user_id not in self.user_prob:
            self.user_prob[user_id] = (1, 1)


        # If this user is new, initialize their click probability
        if user_id not in self.user_prob:
            self.user_prob[user_id] = (1, 1)

        #if num_users > num_rounds. bid nothing
        elif self.num_users > self.num_rounds:
            return 0

        #close to disqualification just sit out
        elif self.balance <= -900:
            return 0

        # If the average winning bid is above $1, bid nothing
        elif self.round_count > self.num_rounds/2 and self.winning_bids \
            and np.mean(self.winning_bids) > 2:
            return 0
        #if the average is too high just sit out
        elif self.winning_bids and np.mean(self.winning_bids) > (1000 + self.balance) * 0.005:
            return 0

        # Estimate the user's click probability
        successes, failures = self.user_prob[user_id]
        estimated_prob = successes / (successes + failures)

        # With probability epsilon, bid between 10 and 100 to explore
        if np.random.uniform() < self.epsilon:
            bid_amount = np.round(np.random.uniform(10,100), 3)
        else:
            # Otherwise, bid proportional to the estimated click probability to exploit
            # but never bid more than $1 or below 0
            bid_amount = max(min(np.round(estimated_prob - 0.05, 3), 1), 0)

        # Decay epsilon
        self.epsilon -= self.decay_rate

        return bid_amount



    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        # If this bidder won the auction, update the user click probability
        if auction_winner:
            successes, failures = self.user_prob[self.current_user_id]

            if clicked:
                successes += 1
            else:
                failures += 1

            self.user_prob[self.current_user_id ] = (successes, failures)
        # Add the winning price to the list of winning bids
        self.winning_bids.append(price)
