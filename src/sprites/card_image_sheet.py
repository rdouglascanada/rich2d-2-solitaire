from rich2d.sprites.images import ImageSheet
from game import Card


class CardImageSheet:
    SUIT_MAP = {
        Card.Suit.SPADES: 0,
        Card.Suit.HEARTS: 1,
        Card.Suit.CLUBS: 2,
        Card.Suit.DIAMONDS: 3
    }

    def __init__(self, file_name=None, image_width=None, image_height=None):
        if file_name is None:
            raise RuntimeError("CardImageSheet file_name cannot be None")
        if image_width is None:
            raise RuntimeError("CardImageSheet image_width cannot be None")
        if image_height is None:
            raise RuntimeError("CardImageSheet image_height cannot be None")

        self._image_sheet = ImageSheet(file_name=file_name, image_width=image_width, image_height=image_height)
        return

    def get_card_image(self, card=None):
        if card is None:
            raise RuntimeError("CardImageSheet.get_card_image card cannot be None")
        x_index = card.get_rank() - 1
        y_index = CardImageSheet.SUIT_MAP[card.get_suit()]
        return self._image_sheet.get_image_at(x_index=x_index, y_index=y_index)

    def get_card_back_image(self):
        return self._image_sheet.get_image_at(x_index=0, y_index=4)
