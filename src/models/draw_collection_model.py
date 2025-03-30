from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite


class DrawCollectionModel(Model):
    def __init__(self, rect=None, selection_manager=None,
                 card_image_sheet=None, deck_draw_manager=None,
                 config_manager=None):
        if rect is None:
            raise RuntimeError("DrawCollectionModel rect cannot be None")
        if selection_manager is None:
            raise RuntimeError("DrawCollectionModel selection_manager cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("DrawCollectionModel card_image_sheet cannot be None")
        if deck_draw_manager is None:
            raise RuntimeError("DrawCollectionModel deck_draw_manager cannot be None")
        if config_manager is None:
            raise RuntimeError("DrawCollectionModel config_manager cannot be None")

        draw_card_collection = deck_draw_manager.get_draw_card_collection()
        draw_collection_sprite = CardCollectionSprite(card_collection=draw_card_collection,
                                                      card_image_sheet=card_image_sheet,
                                                      rect=rect,
                                                      shown=True,
                                                      config_manager=config_manager)

        def on_click():
            selection_manager.select_draw_collection(draw_card_collection)
            return

        mouse_handler = MouseHandler(rect=draw_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click)

        sprites = [draw_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return
