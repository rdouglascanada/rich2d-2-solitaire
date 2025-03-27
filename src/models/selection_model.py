import pygame
from rich2d.models import Model
from rich2d.elements import Element
from rich2d.handlers import MouseHandler
from rich2d.elements.pile import Pile, PileElement
from sprites import CardSprite


class SelectionModel(Model):
    def __init__(self, card_image_sheet=None, selection_manager=None):
        if card_image_sheet is None:
            raise RuntimeError("SelectionModel card_image_sheet cannot be None")
        if selection_manager is None:
            raise RuntimeError("SelectionModel selection_manager cannot be None")

        self._pile = Pile(rect=(0, 0, 80, 120))

        def sync_pile_rect_with_mouse():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pile_rect = self._pile.get_rect()
            pile_rect.x = mouse_x - 20
            pile_rect.y = mouse_y - 20
            return

        def sync_pile_sprites_with_collection():
            card_collection = selection_manager.get_card_collection()
            if len(self._pile) != len(card_collection):
                self._pile.remove_all()
                for card in card_collection.get_cards():
                    card_sprite = CardSprite(card=card, rect=(0, 0, 0, 0),
                                             card_image_sheet=card_image_sheet)
                    self._pile.add(card_sprite)
            return

        def undo_selection():
            selection_manager.undo_selection()
            self._pile.remove_all()
            return

        self._sprite_sync_element = Element(on_update=sync_pile_sprites_with_collection)
        self._mouse_sync_element = Element(on_update=sync_pile_rect_with_mouse)
        self._pile_element = PileElement(pile=self._pile, direction=PileElement.PileElementDirection.DOWN, spacing=20)
        self._mouse_handler = MouseHandler(on_left_mouse_release=undo_selection)
        return

    def get_elements(self):
        return tuple([self._sprite_sync_element, self._mouse_sync_element, self._pile_element])

    def get_sprites(self):
        return self._pile.get_entries()

    def get_handlers(self):
        return tuple([self._mouse_handler])
