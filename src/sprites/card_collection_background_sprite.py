from rich2d.sprites import Sprite
from rich2d.sprites.images import ImageSprite


class CardCollectionBackgroundSprite(Sprite):
    def __init__(self, card_collection_sprite=None, background_image=None):
        if card_collection_sprite is None:
            raise RuntimeError("CardCollectionBackgroundSprite card_collection_sprite cannot be None")
        if background_image is None:
            raise RuntimeError("CardCollectionBackgroundSprite background_image cannot be None")
        super().__init__(rect=card_collection_sprite.get_rect())
        self._card_collection_sprite = card_collection_sprite
        self._background_image = background_image
        self._image_sprite = ImageSprite(rect=card_collection_sprite.get_rect(), image=self._background_image)
        return

    def draw(self, screen):
        self.get_rect().update(self._card_collection_sprite.get_rect())
        self._image_sprite.get_rect().update(self.get_rect())
        self._image_sprite.draw(screen)
        return
