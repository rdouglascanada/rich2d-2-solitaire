from enum import Enum


class Card:
    class Suit(Enum):
        SPADES = 0
        HEARTS = 1
        CLUBS = 2
        DIAMONDS = 3

    class Colour(Enum):
        RED = 0
        BLACK = 1

    def __init__(self, rank=None, suit=None, shown=True):
        if rank is None:
            raise RuntimeError("Card rank cannot be None")
        if suit is None:
            raise RuntimeError("Card suit cannot be None")
        if rank not in Card.get_all_ranks():
            raise RuntimeError(f"Card rank {rank} is not in valid range")
        if suit not in Card.get_all_suits():
            raise RuntimeError(f"Card suit {suit} is not in valid range")

        self._rank = rank
        self._suit = suit
        self._shown = shown
        return

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def get_colour(self):
        if self._suit == Card.Suit.SPADES or self._suit == Card.Suit.CLUBS:
            colour = Card.Colour.BLACK
        elif self._suit == Card.Suit.HEARTS or self._suit == Card.Suit.DIAMONDS:
            colour = Card.Colour.RED
        else:
            raise RuntimeError(f"Card.get_colour unexpected suit {self._suit}")
        return colour

    def show(self):
        self._shown = True
        return

    def hide(self):
        self._shown = False
        return

    def is_shown(self):
        return self._shown

    @staticmethod
    def get_all_suits():
        return tuple([Card.Suit.SPADES, Card.Suit.HEARTS, Card.Suit.CLUBS, Card.Suit.DIAMONDS])

    @staticmethod
    def get_all_ranks():
        return tuple(i for i in range(1, 14))
