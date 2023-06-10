from enum import Enum


class Card:
    class Suit(Enum):
        SPADES = 0
        HEARTS = 1
        CLUBS = 2
        DIAMONDS = 3

    def __init__(self, rank=None, suit=None):
        if rank is None:
            raise RuntimeError("Card rank cannot be None")
        if suit is None:
            raise RuntimeError("Card suit cannot be None")

        self._rank = rank
        self._suit = suit
        return

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit
