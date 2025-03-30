from game import CardCollection
from .logic import DrawSelectionLogic, KlondikeSelectionLogic, SuitSelectionLogic

class SelectionManager:
    def __init__(self, undo_stack=None):
        if undo_stack is None:
            raise RuntimeError("SelectionManager undo_stack cannot be None")
        self._card_collection = CardCollection()
        self._source_selection_logic = None
        self._undo_stack = undo_stack
        return

    def get_card_collection(self):
        return self._card_collection

    def select_draw_collection(self, draw_card_collection):
        selection_card_collection = self._card_collection
        if selection_card_collection.is_empty() and not draw_card_collection.is_empty():
            card = draw_card_collection.draw()
            selection_card_collection.insert(card)
            self._source_selection_logic = DrawSelectionLogic(card_collection=draw_card_collection)
        return

    def select_suit_collection(self, suit_card_collection):
        selection_card_collection = self._card_collection
        if selection_card_collection.is_empty() and not suit_card_collection.is_empty():
            card = suit_card_collection.draw()
            selection_card_collection.insert(card)
            self._source_selection_logic = SuitSelectionLogic(card_collection=suit_card_collection)
        return

    def select_klondike_collection(self, klondike_card_collection, number_of_cards_to_select):
        selection_card_collection = self._card_collection
        if selection_card_collection.is_empty():
            cards_to_select = []
            for i in range(number_of_cards_to_select):
                cards_to_select.append(klondike_card_collection.draw())
            for i in range(number_of_cards_to_select):
                selection_card_collection.insert(cards_to_select.pop())
            self._source_selection_logic = KlondikeSelectionLogic(card_collection=klondike_card_collection)
        return

    def move_cards_to_target_pile(self, target_card_collection, target_selection_logic):
        source_selection_logic = self._source_selection_logic
        selection_card_collection = self._card_collection
        if not target_selection_logic.can_receive_cards(selection_card_collection):
            self.undo_selection()
        else:
            action, undo = source_selection_logic.move_cards(target_card_collection, selection_card_collection)
            action()
            self._undo_stack.push(on_undo=undo)
        return

    def move_cards_to_klondike_pile(self, target_card_collection):
        return self.move_cards_to_target_pile(target_card_collection, KlondikeSelectionLogic(target_card_collection))

    def move_cards_to_suit_pile(self, target_card_collection):
        return self.move_cards_to_target_pile(target_card_collection, SuitSelectionLogic(target_card_collection))

    def undo_selection(self):
        card_collection = self._card_collection
        if not card_collection.is_empty():
            selected_cards = card_collection.remove_all()
            selection_logic = self._source_selection_logic
            last_selected_collection = selection_logic.get_card_collection()
            for card in selected_cards:
                last_selected_collection.insert(card)
        self._source_selection_logic = None
        return