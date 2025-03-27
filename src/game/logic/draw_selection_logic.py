from .selection_logic import SelectionLogic

class DrawSelectionLogic(SelectionLogic):
    def __init__(self, card_collection=None):
        if card_collection is None:
            raise RuntimeError("DrawSelectionLogic card_collection cannot be None")
        self._card_collection = card_collection
        return

    def get_card_collection(self):
        return self._card_collection

    def can_receive_cards(self, selection_card_collection):
        return False

    def move_cards(self, target_card_collection, selection_card_collection):
        if len(selection_card_collection) != 1:
            raise RuntimeError("DrawSelectionLogic.move_cards() number of cards moved must be 1")

        source_card_collection = self._card_collection
        def action():
            target_card_collection.insert(selection_card_collection.draw())
            return

        def undo():
            source_card_collection.insert(target_card_collection.draw())
            return

        return action, undo