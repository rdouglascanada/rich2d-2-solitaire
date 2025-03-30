from rich2d.sprites.images import ImageSheet
from .card import Card

class ConfigManager:
    SUIT_MAP = {
        Card.Suit.SPADES: 0,
        Card.Suit.HEARTS: 1,
        Card.Suit.CLUBS: 2,
        Card.Suit.DIAMONDS: 3
    }

    def __init__(self):
        self._background_colour = "darkgreen"
        self._cardback_image_sheet = ImageSheet(file_name="resources/cardbacks.png",
                                                image_width=80, image_height=120)
        self._cardset_image_sheet = ImageSheet(file_name="resources/cardsets.png",
                                               image_width=80, image_height=120)
        self._cardback_index = 0
        self._cardset_index = 0
        return

    def get_background_colour(self):
        return self._background_colour

    def set_background_colour(self, background_colour):
        self._background_colour = background_colour
        return

    def get_cardback_image(self):
        return self._cardback_image_sheet.get_image_at(x_index=self._cardback_index, y_index=0)

    def get_cardback_image_at(self, index):
        return self._cardback_image_sheet.get_image_at(x_index=index, y_index=0)

    def get_cardback_images(self):
        return self._cardback_image_sheet.get_all_images()

    def get_cardback_index(self):
        return self._cardback_index

    def set_cardback_index(self, index):
        self._cardback_index = index
        return

    def get_card_image_at(self, card=None, index=None):
        if card is None:
            raise RuntimeError("CardImageSheet.get_card_image card cannot be None")
        if index is None:
            raise RuntimeError("CardImageSheet.get_card_image index cannot be None")
        x_index = card.get_rank() - 1
        y_index = ConfigManager.SUIT_MAP[card.get_suit()] + index*len(ConfigManager.SUIT_MAP)
        return self._cardset_image_sheet.get_image_at(x_index=x_index, y_index=y_index)

    def get_card_image(self, card=None):
        return self.get_card_image_at(card, self._cardset_index)

    def get_cardset_index(self):
        return self._cardset_index

    def set_cardset_index(self, index):
        self._cardset_index = index
        return

    @staticmethod
    def background_colour_options():
        return tuple(["darkgreen", "cyan", "magenta", "yellow", "red", "blue", "green", "orange", "purple", "brown",
                      "lightgray", "gray", "black"])