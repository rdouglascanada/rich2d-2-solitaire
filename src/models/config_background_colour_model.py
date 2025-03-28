from pygame import Rect
from rich2d.models import Model, ModelGroup
from rich2d.elements.pile import Pile, PileElement
from game import ConfigManager
from .config_background_colour_choice_model import ConfigBackgroundColourChoiceModel

class ConfigBackgroundColourModel(ModelGroup):
    def __init__(self, rect=None, config_manager=None):
        if rect is None:
            raise RuntimeError("ConfigBackgroundColourModel rect cannot be None")
        if config_manager is None:
            raise RuntimeError("ConfigBackgroundColourModel config_manager cannot be None")

        rect = Rect(rect)
        background_colour_options = ConfigManager.background_colour_options()
        rect_width = rect.w // len(background_colour_options)
        pile = Pile(rect=Rect((rect.x, rect.y, rect_width, rect.h)))
        pile_element = PileElement(pile=pile, direction=PileElement.PileElementDirection.RIGHT, spacing=rect_width)

        choice_models = []
        for colour in background_colour_options:
            choice_model = ConfigBackgroundColourChoiceModel(rect=(0, 0, 0, 0), colour=colour,
                                                             config_manager=config_manager)
            choice_models.append(choice_model)
            pile.add(choice_model)

        pile_model = Model(elements=[pile_element])
        models = [pile_model] + choice_models
        super().__init__(models=models)
        return