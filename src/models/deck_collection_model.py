from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite


class DeckCollectionModel(Model):
    def __init__(self, rect=None, deck_draw_manager=None, config_manager=None):
        if rect is None:
            raise RuntimeError("DeckCollectionModel rect cannot be None")
        if deck_draw_manager is None:
            raise RuntimeError("DeckCollectionModel deck_draw_manager cannot be None")
        if config_manager is None:
            raise RuntimeError("DeckCollectionModel config_manager cannot be None")

        deck_card_collection = deck_draw_manager.get_deck_card_collection()
        deck_collection_sprite = CardCollectionSprite(card_collection=deck_card_collection,
                                                      rect=rect,
                                                      shown=False,
                                                      config_manager=config_manager)
        deck_collection_background_sprite = CardCollectionBackgroundSprite(
            card_collection_sprite=deck_collection_sprite,
            background_image=config_manager.get_deck_collection_background_image())

        def on_click():
            deck_draw_manager.draw_or_refill_deck()
            return

        mouse_handler = MouseHandler(rect=deck_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click)
        sprites = [deck_collection_background_sprite, deck_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return
