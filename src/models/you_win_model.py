from rich2d.models import Model
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import ScaledText

class YouWinModel(Model):
    def __init__(self, rect=None, game_manager=None):
        if rect is None:
            raise RuntimeError("YouWinModel rect cannot be None")
        if game_manager is None:
            raise RuntimeError("YouWinModel game_manager cannot be None")

        self._game_manager = game_manager

        background_rectangle = Rectangle(rect=rect, colour="white")
        text = ScaledText(rect=rect, text="You Win!",
                          font_size=48, font_name="times", font_bold=True)

        super().__init__(sprites=[background_rectangle, text])
        return

    def get_sprites(self):
        if not self._game_manager.is_won():
            return tuple()
        return super().get_sprites()