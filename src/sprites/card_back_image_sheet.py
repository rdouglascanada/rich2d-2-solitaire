from rich2d.sprites.images import ImageSheet

class CardBackImageSheet:
    def __init__(self, file_name=None, image_width=None, image_height=None):
        if file_name is None:
            raise RuntimeError("CardImageSheet file_name cannot be None")
        if image_width is None:
            raise RuntimeError("CardImageSheet image_width cannot be None")
        if image_height is None:
            raise RuntimeError("CardImageSheet image_height cannot be None")

        self._image_sheet = ImageSheet(file_name=file_name, image_width=image_width, image_height=image_height)
        return

    def get_card_back_image(self, x_index, y_index):
        return self._image_sheet.get_image_at(x_index=x_index, y_index=y_index)