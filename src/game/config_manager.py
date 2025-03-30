from rich2d.sprites.images import ImageSheet

class ConfigManager:
    def __init__(self):
        self._background_colour = "darkgreen"
        self._cardback_image_sheet = ImageSheet(file_name="resources/card_sheets/cardbacks.png", image_width=80, image_height=60)
        self._cardback_index = 0
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

    @staticmethod
    def background_colour_options():
        return tuple(["darkgreen", "cyan", "magenta", "yellow", "red", "blue", "green", "orange", "purple", "brown",
                      "lightgray", "gray", "black"])