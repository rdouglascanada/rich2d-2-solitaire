from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite


class SuitCollectionModel(Model):
    def __init__(self, rect=None, selection_manager=None,
                 suit_card_collection=None, background_image=None, config_manager=None):
        if rect is None:
            raise RuntimeError("SuitCollectionModel rect cannot be None")
        if selection_manager is None:
            raise RuntimeError("SuitCollectionModel selection_manager cannot be None")
        if suit_card_collection is None:
            raise RuntimeError("SuitCollectionModel suit_card_collection cannot be None")
        if background_image is None:
            raise RuntimeError("SuitCollectionModel background_image cannot be None")
        if config_manager is None:
            raise RuntimeError("SuitCollectionModel config_manager cannot be None")

        suit_collection_sprite = CardCollectionSprite(card_collection=suit_card_collection,
                                                      rect=rect,
                                                      shown=True,
                                                      config_manager=config_manager)
        suit_collection_background_sprite = CardCollectionBackgroundSprite(
            card_collection_sprite=suit_collection_sprite,
            background_image=background_image)

        def on_click():
            selection_manager.select_suit_collection(suit_card_collection)
            return

        def on_release():
            selection_manager.move_cards_to_suit_pile(suit_card_collection)
            return

        mouse_handler = MouseHandler(rect=suit_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click,
                                     on_left_mouse_release=on_release)
        sprites = [suit_collection_background_sprite, suit_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return
