# Second-Price-Auction

Overview

This project involves developing a bidding algorithm for a second-price auction. The primary goal is to model and simulate an online ad auction where bidders compete to display ads to users. The algorithm balances between exploring (learning how likely users are to click on ads) and exploiting (maximizing immediate rewards by targeting the most promising users). The project involves creating an object-oriented model to simulate the auction and test various bidding strategies.

Project Structure

auction_lastname.py:
Contains the implementation of the Auction class, which manages the rounds of the auction, interactions between bidders and users, and determines the winner of each auction.
bidder_lastname.py:
Contains the implementation of the Bidder class, representing the participants in the auction. Each bidder places bids based on their strategy and can track their balance, winnings, and user click-through rates.
Auction Rules

The auction is a second-price sealed-bid auction, meaning:

Bidders submit bids without knowing what others bid.
The highest bidder wins but pays the second-highest bid price.
Users have a secret click-through probability (between 0 and 1) that remains constant throughout the auction.



Key Features:
Users: Each user has a probability of clicking an ad, drawn from a uniform distribution between 0 and 1.
Bidders: Each bidder starts with a balance and aims to maximize their balance over multiple rounds by winning auctions and displaying ads to users.
Rounds: In each round, a user is selected, bids are placed, and the winner shows their ad to the user. The balance is adjusted based on the user’s interaction (whether they click or not).
