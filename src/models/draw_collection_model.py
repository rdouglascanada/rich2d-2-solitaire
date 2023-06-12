from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite


class DrawCollectionModel(Model):
    def __init__(self, rect=None, selection_model=None, card_image_sheet=None):
        if rect is None:
            raise RuntimeError("DrawCollectionModel rect cannot be None")
        if selection_model is None:
            raise RuntimeError("DrawCollectionModel selection_model cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("DrawCollectionModel card_image_sheet cannot be None")

        draw_collection_sprite = CardCollectionSprite(card_image_sheet=card_image_sheet,
                                                      rect=rect,
                                                      shown=True)
        draw_card_collection = draw_collection_sprite.get_card_collection()
        self._draw_card_collection = draw_card_collection

        def on_click():
            if selection_model.is_empty():
                if not draw_card_collection.is_empty():
                    card = draw_card_collection.draw()
                    selection_model.add_card(card, shown=True)
                    selection_model.set_last_selected_collection(draw_card_collection)
            return

        mouse_handler = MouseHandler(rect=draw_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click)

        sprites = [draw_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return

    def get_card_collection(self):
        return self._draw_card_collection
