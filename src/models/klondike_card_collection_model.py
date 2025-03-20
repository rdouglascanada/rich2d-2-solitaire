import pygame
from rich2d.models import Model
from rich2d.elements import Element
from rich2d.elements.pile import Pile, PileElement
from rich2d.handlers import MouseHandler
from cards import CardCollection
from sprites import CardSprite, CardCollectionBackgroundSprite


class KlondikeCardCollectionModel(Model, CardCollection):
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
        self._background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=self._pile,
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

        def ensure_last_card_sprite_is_always_shown():
            if not self.is_empty() and self._selection_model.is_empty():
                self._pile.get_entries()[-1].show()
            return

        self._show_last_card_element = Element(on_update=ensure_last_card_sprite_is_always_shown)

        def on_release():
            if selection_model.is_empty():
                return
            selected_cards = selection_model.remove_all()
            selected_card = selected_cards[0]
            last_selected_collection = selection_model.get_last_selected_collection()

            if self.is_empty() and selected_card.get_rank() != 13:
                for card in selected_cards:
                    last_selected_collection.insert(card)
            elif self.is_empty():
                for card in selected_cards:
                    self.insert(card)
            else:
                top_card = self.last()
                correct_suit = top_card.get_colour() != selected_card.get_colour()
                correct_rank = top_card.get_rank() - 1 == selected_card.get_rank()
                if correct_rank and correct_suit:
                    for card in selected_cards:
                        self.insert(card)
                else:
                    for card in selected_cards:
                        last_selected_collection.insert(card)
            return

        self._on_release_handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_release=on_release)

        def sync_on_release_handler_rect():
            if not self.is_empty():
                bottom_card_sprite_rect = self._pile.get_entries()[-1].get_rect()
            else:
                bottom_card_sprite_rect = self._rect
            handler_rect = self._on_release_handler.get_rect()
            handler_rect.update(bottom_card_sprite_rect)
            return

        self._sync_release_handler_rect_element = Element(on_update=sync_on_release_handler_rect)
        return

    def hide_all_but_last(self):
        for card_sprite in self._pile.get_entries()[:-1]:
            card_sprite.hide()
        return

    def get_card_collection(self):
        return self

    def is_empty(self):
        return len(self._pile.get_entries()) == 0

    def last(self):
        return self._pile.get_entries()[-1].get_card()

    def first(self):
        return self._pile.get_entries()[0].get_card()

    def get_cards(self):
        return tuple([pe.get_card() for pe in self._pile.get_entries()])

    def __len__(self):
        return len(self._pile.get_entries())

    def insert(self, card):
        card_sprite = CardSprite(rect=(0, 0, 0, 0), shown=True,
                                 card=card, card_image_sheet=self._card_image_sheet)
        self._pile.add(card_sprite)

        def on_click():
            if self._selection_model.is_empty():
                removed_card_sprites = self._pile.remove_after_and_including(card_sprite)
                for rcs in removed_card_sprites:
                    self._on_click_handlers_map.pop(0)
                    self._selection_model.add_card(rcs.get_card())
                self._selection_model.set_last_selected_collection(self)
            return

        handler = MouseHandler(rect=(0, 0, 0, 0), on_left_mouse_click=on_click)
        self._on_click_handlers_map.insert(0, {
            'handler': handler,
            'card_sprite': card_sprite
        })
        return

    def draw(self):
        card_sprite = self._pile.remove(self._pile.get_entries()[0])
        return card_sprite.get_card()

    def get_sprites(self):
        return tuple([self._background_sprite]) + self._pile.get_entries()

    def get_elements(self):
        return tuple([self._pile_element, self._sync_click_handler_rect_element,
                      self._show_last_card_element, self._sync_release_handler_rect_element])

    def get_handlers(self):
        return tuple([self._on_release_handler]) +\
            tuple(value['handler'] for value in self._on_click_handlers_map if value['card_sprite'].is_shown())
