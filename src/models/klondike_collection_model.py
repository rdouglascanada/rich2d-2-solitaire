from rich2d.models import Model
from rich2d.elements import Element
from rich2d.elements.pile import Pile, PileElement
from rich2d.handlers import MouseHandler
from sprites import CardSprite, CardCollectionBackgroundSprite


class KlondikeCollectionModel(Model):
    def __init__(self, rect=None, selection_manager=None,
                 klondike_card_collection=None, config_manager=None):
        if rect is None:
            raise RuntimeError("KlondikeCollectionModel rect cannot be None")
        if selection_manager is None:
            raise RuntimeError("KlondikeCollectionModel selection_manager cannot be None")
        if klondike_card_collection is None:
            raise RuntimeError("KlondikeCollectionModel klondike_card_collection cannot be None")
        if config_manager is None:
            raise RuntimeError("KlondikeCollectionModel config_manager cannot be None")
        self._pile = Pile(rect=rect)
        self._pile_element = PileElement(pile=self._pile,
                                         direction=PileElement.PileElementDirection.DOWN,
                                         spacing=20)
        self._background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=self._pile,
                                                                 background_image=config_manager.\
                                                                 get_card_collection_background_image())
        self._on_click_handlers_map = []
        self._klondike_card_collection = klondike_card_collection
        self._selection_manager = selection_manager
        self._config_manager = config_manager

        def sync_pile_sprites_with_collection():
            card_collection = klondike_card_collection
            discrepancy = len(card_collection) - len(self._pile)
            if discrepancy > 0:
                cards = card_collection.get_cards()[len(self._pile):]
                for i in range(len(cards)):
                    card_sprite = CardSprite(card=cards[i], rect=(0, 0, 0, 0),
                                             config_manager=self._config_manager)
                    self._pile.add(card_sprite)
                self._refresh_click_handlers()
            elif discrepancy < 0:
                start_of_extra_card_sprites = self._pile.get_entries()[discrepancy]
                self._pile.remove(start_of_extra_card_sprites)
                self._refresh_click_handlers()
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
            selection_manager.move_cards_to_klondike_pile(klondike_card_collection)
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
        super().__init__()
        return

    def get_sprites(self):
        return tuple([self._background_sprite]) + self._pile.get_entries()

    def get_elements(self):
        return tuple([self._pile_element, self._sync_pile_sprites_with_collection_element,
                      self._sync_click_handler_rect_element, self._sync_release_handler_rect_element])

    def get_handlers(self):
        return tuple([self._on_release_handler]) +\
            tuple(value['handler'] for value in self._on_click_handlers_map \
                  if value['card_sprite'].get_card().is_shown())

    def refresh(self):
        self._pile.remove_all()
        for card in self._klondike_card_collection.get_cards():
            card_sprite = CardSprite(card=card, rect=(0, 0, 0, 0),
                                     config_manager=self._config_manager)
            self._pile.add(card_sprite)
        self._refresh_click_handlers()
        return

    def _add_click_handler(self, card_sprite, number_of_cards_to_select):
        def on_click():
            self._selection_manager.select_klondike_collection(self._klondike_card_collection, number_of_cards_to_select)
            return

        handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_click=on_click)
        self._on_click_handlers_map.insert(0, {
            'handler': handler,
            'card_sprite': card_sprite
        })
        return

    def _refresh_click_handlers(self):
        self._on_click_handlers_map.clear()
        pile_entries = self._pile.get_entries()
        for i in range(len(self._klondike_card_collection)):
            card_sprite = pile_entries[i]
            self._add_click_handler(card_sprite, len(self._klondike_card_collection) - i)
        return
