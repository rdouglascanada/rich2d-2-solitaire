from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite
from game import CardCollection
from game.logic import SuitSelectionLogic
from .klondike_collection_model import KlondikeCollectionModel


class SuitCollectionModel(Model):
    def __init__(self, rect=None, selection_manager=None, card_image_sheet=None,
                 suit_card_collection=None, background_image=None, undo_stack=None):
        if rect is None:
            raise RuntimeError("SuitCollectionModel rect cannot be None")
        if selection_manager is None:
            raise RuntimeError("SuitCollectionModel selection_manager cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("SuitCollectionModel card_image_sheet cannot be None")
        if suit_card_collection is None:
            raise RuntimeError("SuitCollectionModel suit_card_collection cannot be None")
        if background_image is None:
            raise RuntimeError("SuitCollectionModel background_image cannot be None")
        if undo_stack is None:
            raise RuntimeError("SuitCollectionModel undo_stack cannot be None")

        suit_collection_sprite = CardCollectionSprite(card_collection=suit_card_collection,
                                                      card_image_sheet=card_image_sheet,
                                                      rect=rect,
                                                      shown=True)
        suit_collection_background_sprite = CardCollectionBackgroundSprite(
            card_collection_sprite=suit_collection_sprite,
            background_image=background_image)
        suit_selection_logic = SuitSelectionLogic(card_collection=suit_card_collection)

        def on_click():
            selection_card_collection = selection_manager.get_card_collection()
            if selection_card_collection.is_empty() and not suit_card_collection.is_empty():
                card = suit_card_collection.draw()
                selection_card_collection.insert(card)
                selection_manager.set_selection_logic(suit_selection_logic)
            return

        def on_release():
            selection_card_collection = selection_manager.get_card_collection()
            if not suit_selection_logic.can_receive_cards(selection_card_collection):
                selection_manager.undo_selection()
            else:
                selection_logic = selection_manager.get_selection_logic()
                action, undo = selection_logic.move_cards(suit_card_collection, selection_card_collection)
                action()
                undo_stack.push(on_undo=undo)
            return

        mouse_handler = MouseHandler(rect=suit_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click,
                                     on_left_mouse_release=on_release)
        sprites = [suit_collection_background_sprite, suit_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return
