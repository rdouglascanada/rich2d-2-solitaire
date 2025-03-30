from rich2d.sprites import Sprite
from rich2d.sprites.images import ImageSprite


class CardSprite(Sprite):
    def __init__(self, rect=None, card=None, config_manager=None):
        if rect is None:
            raise RuntimeError("CardSprite rect cannot be None")
        if card is None:
            raise RuntimeError("CardSprite card cannot be None")
        if config_manager is None:
            raise RuntimeError("CardSprite config_manager cannot be None")
        super().__init__(rect=rect)
        self._card = card
        self._config_manager = config_manager
        self._front_sprite = ImageSprite(image=config_manager.get_card_image(card=card), rect=rect)
        self._back_sprite = ImageSprite(image=config_manager.get_cardback_image(), rect=rect)
        return

    def draw(self, screen):
        self._front_sprite.get_rect().update(self.get_rect())
        self._back_sprite.get_rect().update(self.get_rect())
        self._front_sprite.set_image(self._config_manager.get_card_image(self._card))
        self._back_sprite.set_image(self._config_manager.get_cardback_image())

        if self._card.is_shown():
            self._front_sprite.draw(screen)
        else:
            self._back_sprite.draw(screen)
        return

    def get_card(self):
        return self._card
