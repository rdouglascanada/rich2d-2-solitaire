from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite


class DeckCollectionModel(Model):
    def __init__(self, rect=None, selection_model=None, card_image_sheet=None, background_image=None,
                 draw_collection_model=None, undo_stack=None):
        if rect is None:
            raise RuntimeError("DeckCollectionModel rect cannot be None")
        if selection_model is None:
            raise RuntimeError("DeckCollectionModel selection_model cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("DeckCollectionModel card_image_sheet cannot be None")
        if background_image is None:
            raise RuntimeError("DeckCollectionModel background_image cannot be None")
        if draw_collection_model is None:
            raise RuntimeError("DeckCollectionModel draw_collection_model cannot be None")
        if undo_stack is None:
            raise RuntimeError("DeckCollectionModel undo_stack cannot be None")

        deck_collection_sprite = CardCollectionSprite(card_image_sheet=card_image_sheet,
                                                      rect=rect,
                                                      shown=False)
        deck_collection_background_sprite = CardCollectionBackgroundSprite(
            card_collection_sprite=deck_collection_sprite,
            background_image=background_image)
        deck_card_collection = deck_collection_sprite.get_card_collection()
        self._deck_card_collection = deck_card_collection

        def on_click():
            draw_card_collection = draw_collection_model.get_card_collection()
            if not deck_card_collection.is_empty():
                draw_card_collection.insert(deck_card_collection.draw())
                def undo_card_draw():
                    deck_card_collection.insert(draw_card_collection.draw())
                    return
                undo_stack.push(on_undo=undo_card_draw)
            else:
                while not draw_card_collection.is_empty():
                    deck_card_collection.insert(draw_card_collection.draw())
                def undo_deck_refill():
                    while not deck_card_collection.is_empty():
                        draw_card_collection.insert(deck_card_collection.draw())
                    return
                undo_stack.push(on_undo=undo_deck_refill)
            return

        mouse_handler = MouseHandler(rect=deck_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click)

        sprites = [deck_collection_background_sprite, deck_collection_sprite]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, handlers=handlers)
        return

    def get_card_collection(self):
        return self._deck_card_collection

    def remove_all(self):
        return self._deck_card_collection.remove_all()
