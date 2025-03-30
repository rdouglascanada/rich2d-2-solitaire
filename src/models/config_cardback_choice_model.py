from pygame import Rect
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.images import ImageSprite
from rich2d.models import Model
from rich2d.elements import Element
from rich2d.handlers import MouseHandler

class ConfigCardbackChoiceModel(Model):
    def __init__(self, rect=None, index=None, config_manager=None):
        if rect is None:
            raise RuntimeError("ConfigCardbackChoiceModel rect cannot be None")
        if index is None:
            raise RuntimeError("ConfigCardbackChoiceModel index cannot be None")
        if config_manager is None:
            raise RuntimeError("ConfigCardbackChoiceModel config_manager cannot be None")
        self._rect = Rect(rect)
        self._inner_rect = self._rect.inflate(-10, -10)
        self._index = index

        outer_rectangle = Rectangle(rect=self._rect)
        cardback_sprite = ImageSprite(image=config_manager.get_cardback_image_at(index), rect=self._inner_rect)

        def on_left_click():
            config_manager.set_cardback_index(index)
            return
        mouse_handler = MouseHandler(rect=self._rect, on_left_mouse_click=on_left_click)

        def sync_rects():
            self._inner_rect.update(self._rect.inflate(-10, -10))
            outer_rectangle.get_rect().update(self._rect)
            cardback_sprite.get_rect().update(self._inner_rect)
            mouse_handler.get_rect().update(self._rect)
            return
        sync_rect_element = Element(on_update=sync_rects)

        def set_outer_colour():
            if index == config_manager.get_cardback_index():
                outer_rectangle.set_colour((50, 50, 50))
            else:
                outer_rectangle.set_colour((175, 175, 175))
            return
        outer_colour_element = Element(on_update=set_outer_colour)

        sprites = [outer_rectangle, cardback_sprite]
        elements = [sync_rect_element, outer_colour_element]
        handlers = [mouse_handler]
        super().__init__(sprites=sprites, elements=elements, handlers=handlers)
        return

    def get_rect(self):
        return self._rect