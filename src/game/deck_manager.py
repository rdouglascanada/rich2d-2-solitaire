class DeckManager:
    def __init__(self, deck_card_collection=None, draw_card_collection=None, undo_stack=None):
        if deck_card_collection is None:
            raise RuntimeError("DeckManager deck_card_collection cannot be None")
        if draw_card_collection is None:
            raise RuntimeError("DeckManager draw_card_collection cannot be None")
        if undo_stack is None:
            raise RuntimeError("DeckManager undo_stack cannot be None")
        self._deck_card_collection = deck_card_collection
        self._draw_card_collection = draw_card_collection
        self._undo_stack = undo_stack
        return

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
