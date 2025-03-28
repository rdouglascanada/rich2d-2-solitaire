class ConfigManager:
    def __init__(self):
        self._background_colour = "darkgreen"
        return

    def get_background_colour(self):
        return self._background_colour

    def set_background_colour(self, background_colour):
        self._background_colour = background_colour
        return

    @staticmethod
    def background_colour_options():
        return tuple(["darkgreen", "cyan", "magenta", "yellow", "red", "blue", "green", "orange", "purple", "brown",
                      "black", "gray"])