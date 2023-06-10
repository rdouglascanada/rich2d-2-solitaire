from enum import IntEnum
from rich2d.sprites.images import ImageSheet


class CardImageSheet:
    class Suit(IntEnum):
        SPADES = 0
        HEARTS = 1
        CLUBS = 2
        DIAMONDS = 3

    def __init__(self, file_name=None, image_width=None, image_height=None):
        if file_name is None:
            raise RuntimeError("CardImageSheet file_name cannot be None")
        if image_width is None:
            raise RuntimeError("CardImageSheet image_width cannot be None")
        if image_height is None:
            raise RuntimeError("CardImageSheet image_height cannot be None")

        self._image_sheet = ImageSheet(file_name=file_name, image_width=image_width, image_height=image_height)
        return

    def get_card_image(self, rank=None, suit=None):
        if rank is None:
            raise RuntimeError("CardImageSheet.get_card_image rank cannot be None")
        if suit is None:
            raise RuntimeError("CardImageSheet.get_card_image suit cannot be None")
        return self._image_sheet.get_image_at(x_index=int(rank) - 1, y_index=int(suit))

    def get_card_back_image(self):
        return self._image_sheet.get_image_at(x_index=0, y_index=4)
