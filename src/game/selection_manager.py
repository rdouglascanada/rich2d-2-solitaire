from game import CardCollection

class SelectionManager:
    def __init__(self):
        self._card_collection = CardCollection()
        self._selection_logic = None
        return

    def get_card_collection(self):
        return self._card_collection

    def get_selection_logic(self):
        return self._selection_logic

    def set_selection_logic(self, selection_logic):
        self._selection_logic = selection_logic
        return

    def undo_selection(self):
        card_collection = self._card_collection
        if not card_collection.is_empty():
            selected_cards = card_collection.remove_all()
            selection_logic = self._selection_logic
            last_selected_collection = selection_logic.get_card_collection()
            for card in selected_cards:
                last_selected_collection.insert(card)
        self._selection_logic = None
        return