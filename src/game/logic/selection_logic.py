from abc import ABC, abstractmethod

class SelectionLogic:
    @abstractmethod
    def get_card_collection(self):
        pass

    @abstractmethod
    def can_receive_cards(self, selection_card_collection):
        pass

    @abstractmethod
    def move_cards(self, target_card_collection, selection_card_collection):
        return