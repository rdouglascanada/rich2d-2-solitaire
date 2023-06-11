class CardCollection:
    def __init__(self, cards=[]):
        self._cards = list(cards)
        return

    def insert(self, card):
        self._cards.append(card)
        return

    def draw(self):
        card = self._cards.pop()
        return card

    def peek(self):
        return self._cards[-1]

    def is_empty(self):
        return len(self._cards) == 0

    def get_cards(self):
        return tuple(self._cards)
