import pygame
from rich2d.models import Model
from rich2d.elements import Element
from rich2d.elements.pile import Pile, PileElement
from rich2d.handlers import MouseHandler
from sprites import CardSprite, CardCollectionBackgroundSprite


class KlondikePileModel(Model):
    def __init__(self, rect=None, selection_model=None, card_image_sheet=None, background_image=None):
        if rect is None:
            raise RuntimeError("KlondikePileModel rect cannot be None")
        if selection_model is None:
            raise RuntimeError("KlondikePileModel selection_model cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("KlondikePileModel card_image_sheet cannot be None")
        if background_image is None:
            raise RuntimeError("KlondikePileModel background_image cannot be None")
        self._rect = pygame.Rect(rect)
        self._pile = Pile(rect=rect)
        self._pile_element = PileElement(pile=self._pile,
                                         direction=PileElement.PileElementDirection.DOWN,
                                         spacing=20)
        self._background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=self,
                                                                 background_image=background_image)
        self._selection_model = selection_model
        self._card_image_sheet = card_image_sheet
        self._on_click_handlers_map = []

        def sync_click_handler_rects():
            for value in self._on_click_handlers_map:
                card_sprite_rect = value['card_sprite'].get_rect()
                handler_rect = value['handler'].get_rect()
                handler_rect.update(card_sprite_rect)

        self._sync_click_handler_rect_element = Element(on_update=sync_click_handler_rects)
        return

    def insert(self, card, shown=True):
        card_sprite = CardSprite(rect=(0, 0, 0, 0), shown=shown,
                                 card=card, card_image_sheet=self._card_image_sheet)
        self._pile.add(card_sprite)
        if shown:
            def on_click():
                if self._selection_model.is_empty():
                    removed_card_sprites = self._pile.remove_after_and_including(card_sprite)
                    for rcs in removed_card_sprites:
                        self._on_click_handlers.pop(0)
                        self._selection_model.add_card(rcs.get_card())
                    card_sprite_to_show = None
                    if not self._pile.is_empty():
                        card_sprite_to_show = self._pile.get_entries()[-1]
                    self._selection_model.set_card_sprite_to_show(card_sprite_to_show)
                return

            handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_click=on_click)
            self._on_click_handlers_map.insert(0, {
                'handler': handler,
                'card_sprite': card_sprite
            })
        return

    def get_rect(self):
        return self._rect

    def get_sprites(self):
        return tuple([self._background_sprite]) + self._pile.get_entries()

    def get_elements(self):
        return tuple([self._pile_element, self._sync_click_handler_rect_element])

    def get_handlers(self):
        return tuple(value['handler'] for value in self._on_click_handlers_map)
