from random import shuffle
from .card import Card


class Deck:
    def __init__(self):
        self._cards = []
        for suit in Card.get_all_suits():
            for rank in Card.get_all_ranks():
                self._cards.append(Card(rank=rank, suit=suit))
        return

    def shuffle(self):
        shuffle(self._cards)
        return

    def get_cards(self):
        return tuple(self._cards)
