from rich2d.sprites import Sprite
from .card_sprite import CardSprite
from game import CardCollection


class CardCollectionSprite(Sprite):
    def __init__(self, rect=None, card_image_sheet=None, card_collection=None, shown=True):
        if rect is None:
            raise RuntimeError("CardCollectionSprite rect cannot be None")
        if card_image_sheet is None:
            raise RuntimeError("CardCollectionSprite card_image_sheet cannot be None")
        if card_collection is None:
            card_collection = CardCollection()
        super().__init__(rect=rect)
        self._card_image_sheet = card_image_sheet
        self._card_collection = card_collection
        self._shown = shown
        return

    def get_card_collection(self):
        return self._card_collection

    def draw(self, screen):
        if self._card_collection.is_empty():
            return
        card_sprite = CardSprite(rect=self.get_rect(), card=self._card_collection.last(),
                                 card_image_sheet=self._card_image_sheet, shown=self._shown)
        card_sprite.draw(screen)
        return

