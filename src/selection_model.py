import pygame
from rich2d.models import Model
from rich2d.elements import Element
from rich2d.elements.pile import Pile, PileElement
from sprites import CardSprite


class SelectionModel(Model):
    def __init__(self, card_image_sheet=None):
        if card_image_sheet is None:
            raise RuntimeError("SelectionModel card_image_sheet cannot be None")

        self._card_image_sheet = card_image_sheet
        self._pile = Pile(rect=(0, 0, 80, 120))

        def sync_pile_rect_with_mouse():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pile_rect = self._pile.get_rect()
            pile_rect.x = mouse_x - 20
            pile_rect.y = mouse_y - 20
            return

        self._mouse_sync_element = Element(on_update=sync_pile_rect_with_mouse)
        self._pile_element = PileElement(pile=self._pile, direction=PileElement.PileElementDirection.DOWN, spacing=20)
        self._last_selected_collection = None
        return

    def is_empty(self):
        return self._pile.is_empty()

    def __len__(self):
        return len(self._pile)

    def get_last_selected_collection(self):
        return self._last_selected_collection

    def set_last_selected_collection(self, card_collection):
        self._last_selected_collection = card_collection
        return

    def add_card(self, card, shown=True):
        card_sprite = CardSprite(card=card, rect=(0, 0, 0, 0),
                                 card_image_sheet=self._card_image_sheet, shown=shown)
        self._pile.add(card_sprite)
        return

    def remove_all(self):
        card_sprites = self._pile.remove_all()
        cards = [card_sprite.get_card() for card_sprite in card_sprites]
        return cards

    def get_elements(self):
        return tuple([self._mouse_sync_element, self._pile_element])

    def get_sprites(self):
        return self._pile.get_entries()

    def get_handlers(self):
        return tuple([])
