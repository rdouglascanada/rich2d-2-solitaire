from game import CardCollection

class DeckDrawManager:
    def __init__(self, undo_stack=None):
        if undo_stack is None:
            raise RuntimeError("DeckDrawManager undo_stack cannot be None")
        self._deck_card_collection = CardCollection()
        self._draw_card_collection = CardCollection()
        self._undo_stack = undo_stack
        return

    def get_deck_card_collection(self):
        return self._deck_card_collection

    def get_draw_card_collection(self):
        return self._draw_card_collection

    def draw_or_refill_deck(self):
        deck_card_collection = self._deck_card_collection
        if not deck_card_collection.is_empty():
            self.draw_card()
        else:
            self.refill_deck()
        return

    def draw_card(self):
        deck_card_collection = self._deck_card_collection
        draw_card_collection = self._draw_card_collection
        undo_stack = self._undo_stack

        draw_card_collection.insert(deck_card_collection.draw())

        def undo_card_draw():
            deck_card_collection.insert(draw_card_collection.draw())
            return

        undo_stack.push(on_undo=undo_card_draw)
        return

    def refill_deck(self):
        deck_card_collection = self._deck_card_collection
        draw_card_collection = self._draw_card_collection
        undo_stack = self._undo_stack

        while not draw_card_collection.is_empty():
            deck_card_collection.insert(draw_card_collection.draw())

        def undo_deck_refill():
            while not deck_card_collection.is_empty():
                draw_card_collection.insert(deck_card_collection.draw())
            return

        undo_stack.push(on_undo=undo_deck_refill)
        return
