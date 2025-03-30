from .deck import Deck
from .card_collection import CardCollection
from .undo_stack import UndoStack
from .deck_draw_manager import DeckDrawManager
from .selection_manager import SelectionManager

class GameManager:
    def __init__(self):
        self._deck = Deck()
        self._undo_stack = UndoStack()
        self._selection_manager = SelectionManager()
        self._deck_draw_manager = DeckDrawManager(undo_stack=self._undo_stack)
        self._suit_card_collections = [CardCollection(), CardCollection(), CardCollection(), CardCollection()]
        self._klondike_card_collections = [CardCollection(), CardCollection(), CardCollection(),
                                           CardCollection(), CardCollection(), CardCollection(),
                                           CardCollection()]
        return

    def new_game(self):
        card_collections = [self._deck_draw_manager.get_deck_card_collection(),
                            self._deck_draw_manager.get_draw_card_collection(),
                            self._selection_manager.get_card_collection()] + \
                           self._suit_card_collections + self._klondike_card_collections
        for card_collection in card_collections:
            card_collection.remove_all()
        self._undo_stack.remove_all()

        self._deck.shuffle()
        cards = self._deck.get_cards()
        deck_card_collection = self._deck_draw_manager.get_deck_card_collection()

        c = 0
        for i in range(len(self._klondike_card_collections)):
            card_collection = self._klondike_card_collections[i]
            for j in range(i + 1):
                card_collection.insert(cards[c])
                cards[c].hide()
                c += 1
            cards[c - 1].show()

        for card in cards[c:]:
            deck_card_collection.insert(card)
        return

    def get_undo_stack(self):
        return self._undo_stack

    def get_selection_manager(self):
        return self._selection_manager

    def get_deck_draw_manager(self):
        return self._deck_draw_manager

    def get_suit_card_collections(self):
        return self._suit_card_collections

    def get_klondike_card_collections(self):
        return self._klondike_card_collections

    def is_won(self):
        total_number_of_cards = len(self._deck.get_cards())
        number_of_cards_in_suit_collections = 0
        for suit_collection in self._suit_card_collections:
            number_of_cards_in_suit_collections += len(suit_collection)
        return number_of_cards_in_suit_collections == total_number_of_cards