from rich2d.models import Model
from rich2d.handlers import MouseHandler
from sprites import CardCollectionSprite, CardCollectionBackgroundSprite
from .klondike_card_collection_model import KlondikeCardCollectionModel


class SuitCollectionModel(Model):
    def __init__(self, rect=None, selection_model=None, card_image_sheet=None, background_image=None, undo_stack=None):
        if rect is None:
            raise RuntimeError("SuitCollectionModel rect cannot be None")
        if selection_model is None:
            raise RuntimeError("SuitCollectionModel selection_model cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("SuitCollectionModel card_image_sheet cannot be None")
        if background_image is None:
            raise RuntimeError("SuitCollectionModel background_image cannot be None")
        if undo_stack is None:
            raise RuntimeError("SuitCollectionModel undo_stack cannot be None")

        suit_collection_sprite = CardCollectionSprite(card_image_sheet=card_image_sheet,
                                                      rect=rect,
                                                      shown=True)
        suit_collection_background_sprite = CardCollectionBackgroundSprite(
            card_collection_sprite=suit_collection_sprite,
            background_image=background_image)

        def on_click():
            if selection_model.is_empty():
                card_collection = suit_collection_sprite.get_card_collection()
                if not card_collection.is_empty():
                    card = card_collection.draw()
                    selection_model.add_card(card, shown=True)
                    selection_model.set_last_selected_collection(card_collection)
            return

        def on_release():
            if selection_model.is_empty():
                return
            if len(selection_model) > 1:
                selected_cards = selection_model.remove_all()
                last_selected_collection = selection_model.get_last_selected_collection()
                for card in selected_cards:
                    last_selected_collection.insert(card)
                return
            selected_card = selection_model.remove_all()[0]
            suit_collection = suit_collection_sprite.get_card_collection()
            last_selected_collection = selection_model.get_last_selected_collection()
            if isinstance(last_selected_collection, KlondikeCardCollectionModel):
                shown_count = 1
                for card_sprite in last_selected_collection._pile.get_entries():
                    if card_sprite.is_shown():
                        shown_count += 1

            def move_card_back():
                last_selected_collection.insert(suit_collection.draw())
                if isinstance(last_selected_collection, KlondikeCardCollectionModel):
                    s = 0
                    entries = last_selected_collection._pile.get_entries()
                    for sprite in entries:
                        if s + shown_count < len(entries):
                            sprite.hide()
                        else:
                            sprite.show()
                        s += 1
                return

            if suit_collection.is_empty() and selected_card.get_rank() != 1:
                last_selected_collection.insert(selected_card)
            elif suit_collection.is_empty():
                suit_collection.insert(selected_card)
                undo_stack.push(on_undo=move_card_back)
            else:
                top_card = suit_collection.last()
                correct_suit = top_card.get_suit() == selected_card.get_suit()
                correct_rank = top_card.get_rank() + 1 == selected_card.get_rank()
                if correct_rank and correct_suit:
                    suit_collection.insert(selected_card)
                    undo_stack.push(on_undo=move_card_back)
                else:
                    last_selected_collection.insert(selected_card)
            return

        mouse_handler = MouseHandler(rect=suit_collection_sprite.get_rect(),
                                     on_left_mouse_click=on_click,
                                     on_left_mouse_release=on_release)

        sprites = [suit_collection_background_sprite, suit_collection_sprite]
        handlers = [mouse_handler]
        self._card_collection = suit_collection_sprite.get_card_collection()
        super().__init__(sprites=sprites, handlers=handlers)
        return

    def remove_all(self):
        return self._card_collection.remove_all()
