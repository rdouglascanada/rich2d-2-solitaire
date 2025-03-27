from .selection_logic import SelectionLogic

class KlondikeSelectionLogic(SelectionLogic):
    def __init__(self, card_collection=None):
        if card_collection is None:
            raise RuntimeError("KlondikeSelectionLogic card_collection cannot be None")
        self._card_collection = card_collection
        return

    def get_card_collection(self):
        return self._card_collection

    def can_receive_cards(self, selection_card_collection):
        if selection_card_collection.is_empty():
            return False
        card_at_base_of_selection = selection_card_collection.first()

        target_card_collection = self._card_collection
        if target_card_collection.is_empty():
            return card_at_base_of_selection.get_rank() == 13
        card_at_target = target_card_collection.last()

        correct_suit = card_at_target.get_colour() != card_at_base_of_selection.get_colour()
        correct_rank = card_at_target.get_rank() - 1 == card_at_base_of_selection.get_rank()
        return correct_suit and correct_rank

    def move_cards(self, target_card_collection, selection_card_collection):
        cards = selection_card_collection.remove_all()
        source_card_collection = self._card_collection

        if source_card_collection.is_empty():
            show_new_card = False
        else:
            new_card_at_top = source_card_collection.last()
            show_new_card = not new_card_at_top.is_shown()

        def action():
            for card in cards:
                target_card_collection.insert(card)
            if show_new_card:
                new_card_at_top.show()
            return

        def undo():
            for card in cards:
                source_card_collection.insert(card)
                target_card_collection.draw()
            if show_new_card:
                new_card_at_top.hide()
            return

        return action, undo