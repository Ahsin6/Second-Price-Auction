"""Auction Class"""

import numpy as np


class User:
    """Class to represent a user with a secret probability of clicking an ad."""

    def __init__(self):
        """Generating a probability between 0 and 1 from a uniform distribution"""
        self.__probability = np.random.uniform()

    def __repr__(self):
        """User object with secret probability"""
        return self.__str__()

    def __str__(self):
        """User object with a secret likelihood of clicking on an ad"""
        return f"{self.__probability}"

    def show_ad(self):
        """Returns True to represent the user clicking on an ad or False otherwise"""
        return np.random.uniform() <= self.__probability


class Auction:
    """Class to represent an online second-price ad auction"""

    def __init__(self, users, bidders):
        """Initializing users, bidders,
        and dictionary to store balances for each bidder in the auction"""
        self.users = users
        self.bidders = bidders
        self.balances = {bidder: 0 for bidder in self.bidders}

    def __repr__(self):
        """Return string representation of the auction object"""
        return self.__str__()

    def __str__(self):
        """Return string representation of the auction object"""
        return f"Users: {self.users}, Bidders: {self.bidders}"

    def qualified_bidders(self):
        """Checks if the bidders is still qualified. If the bidder balance falls bellow -1000,
        remove bidder from the auction."""
        return {bidder: bal for bidder, bal in self.balances.items() if bal >= -1000}

    def execute_round(self):
        """Executes a single round of an auction, completing the following steps:
        - random user selection
        - bids from every qualified bidder in the auction
        - selection of winning bidder based on maximum bid
        - selection of actual price (second-highest bid)
        - showing ad to user and finding out whether or not they click
        - notifying winning bidder of price and user outcome and updating balance
        - notifying losing bidders of price"""
        # Pick a random User
        user = np.random.choice(self.users)
        # Gather all bids from qualified bidders
        bids = [(bidder, bidder.bid(user)) for bidder in self.qualified_bidders()]
        # Sort bids based on price
        bids = sorted(bids, key=lambda x: x[1], reverse=True)
        # Keep track of max bid
        max_bid = bids[0][1]
        # If more than one max bid
        check_winner = [i for i in range(len(bids)) if bids[i][1] == max_bid]
        # Winning bid is the first bidder,
        # if more than one max bidder choose randomly
        winning_bid = (
            bids.pop(0)
            if len(check_winner) > 1
            else bids.pop(np.random.choice(check_winner))
        )
        # Gather second highest price
        price = bids[0][1] if len(bids) > 1 and bids[0][1] != 0 else winning_bid[1]

        show_ad = user.show_ad()

        # If User clicked on the ad.
        if show_ad:
            winning_bid[0].notify(True, price, show_ad)
            self.balances[winning_bid[0]] += 1
            self.balances[winning_bid[0]] -= price
        else:
            winning_bid[0].notify(True, price, show_ad)
            self.balances[winning_bid[0]] -= price
        # Alert all other bidders
        for bidder in bids:
            bidder[0].notify(False, price, None)
