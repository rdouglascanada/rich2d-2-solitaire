from rich2d.models import Model
from rich2d.elements import Element
from rich2d.elements.pile import Pile, PileElement
from rich2d.handlers import MouseHandler
from sprites import CardSprite, CardCollectionBackgroundSprite
from game.logic import KlondikeSelectionLogic


class KlondikeCollectionModel(Model):
    def __init__(self, rect=None, selection_manager=None, card_image_sheet=None,
                 klondike_card_collection=None, background_image=None, undo_stack=None):
        if rect is None:
            raise RuntimeError("KlondikeCollectionModel rect cannot be None")
        if selection_manager is None:
            raise RuntimeError("KlondikeCollectionModel selection_manager cannot be None")
        if klondike_card_collection is None:
            raise RuntimeError("KlondikeCollectionModel klondike_card_collection cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("KlondikeCollectionModel card_image_sheet cannot be None")
        if background_image is None:
            raise RuntimeError("KlondikeCollectionModel background_image cannot be None")
        if undo_stack is None:
            raise RuntimeError("KlondikeCollectionModel undo_stack cannot be None")
        self._pile = Pile(rect=rect)
        self._pile_element = PileElement(pile=self._pile,
                                         direction=PileElement.PileElementDirection.DOWN,
                                         spacing=20)
        self._background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=self._pile,
                                                                 background_image=background_image)
        self._on_click_handlers_map = []
        klondike_selection_logic = KlondikeSelectionLogic(card_collection=klondike_card_collection)

        def sync_pile_sprites_with_collection():
            card_collection = klondike_card_collection
            if len(self._pile) != len(card_collection):
                self._pile.remove_all()
                self._on_click_handlers_map.clear()

                i = 0
                for card in card_collection.get_cards():
                    card_sprite = CardSprite(card=card, rect=(0, 0, 0, 0),
                                             card_image_sheet=card_image_sheet)
                    self._pile.add(card_sprite)
                    self._add_click_handler(card_sprite, card_collection, selection_manager,
                                            klondike_selection_logic, len(card_collection) - i)
                    i += 1
            return

        self._sync_pile_sprites_with_collection_element = Element(on_update=sync_pile_sprites_with_collection)

        def sync_click_handler_rects():
            for value in self._on_click_handlers_map:
                card_sprite_rect = value['card_sprite'].get_rect()
                handler_rect = value['handler'].get_rect()
                handler_rect.update(card_sprite_rect)
            return

        self._sync_click_handler_rect_element = Element(on_update=sync_click_handler_rects)

        def on_release():
            selection_card_collection = selection_manager.get_card_collection()
            if not klondike_selection_logic.can_receive_cards(selection_card_collection):
                selection_manager.undo_selection()
            else:
                selection_logic = selection_manager.get_selection_logic()
                action, undo = selection_logic.move_cards(klondike_card_collection, selection_card_collection)
                action()
                undo_stack.push(on_undo=undo)
            return

        self._on_release_handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_release=on_release)

        def sync_on_release_handler_rect():
            if not self._pile.is_empty():
                bottom_card_sprite_rect = self._pile.get_entries()[-1].get_rect()
            else:
                bottom_card_sprite_rect = self._pile.get_rect()
            handler_rect = self._on_release_handler.get_rect()
            handler_rect.update(bottom_card_sprite_rect)
            return

        self._sync_release_handler_rect_element = Element(on_update=sync_on_release_handler_rect)
        return

    def get_sprites(self):
        return tuple([self._background_sprite]) + self._pile.get_entries()

    def get_elements(self):
        return tuple([self._pile_element, self._sync_pile_sprites_with_collection_element,
                      self._sync_click_handler_rect_element, self._sync_release_handler_rect_element])

    def get_handlers(self):
        return tuple([self._on_release_handler]) +\
            tuple(value['handler'] for value in self._on_click_handlers_map if value['card_sprite'].get_card().is_shown())

    def _add_click_handler(self, card_sprite, card_collection, selection_manager,
                           klondike_selection_logic, number_of_cards_to_select):
        def on_click():
            selection_card_collection = selection_manager.get_card_collection()
            if selection_card_collection.is_empty():
                cards_to_select = []
                for j in range(number_of_cards_to_select):
                    cards_to_select.append(card_collection.draw())
                for j in range(number_of_cards_to_select):
                    selection_card_collection.insert(cards_to_select.pop())
                selection_manager.set_selection_logic(klondike_selection_logic)
            return


        handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_click=on_click)
        self._on_click_handlers_map.insert(0, {
            'handler': handler,
            'card_sprite': card_sprite
        })
        return
