from pygame import Rect
from rich2d.models import Model, ModelGroup
from rich2d.elements.pile import Pile, PileElement
from .config_cardback_choice_model import ConfigCardbackChoiceModel

class ConfigCardbackModel(ModelGroup):
    def __init__(self, rect=None, config_manager=None):
        if rect is None:
            raise RuntimeError("ConfigCardbackModel rect cannot be None")
        if config_manager is None:
            raise RuntimeError("ConfigCardbackModel config_manager cannot be None")

        rect = Rect(rect)
        cardback_options = config_manager.get_cardback_images()
        rect_width = rect.w // len(cardback_options)
        pile = Pile(rect=Rect((rect.x, rect.y, rect_width, rect.h)))
        pile_element = PileElement(pile=pile, direction=PileElement.PileElementDirection.RIGHT, spacing=rect_width)

        choice_models = []
        for i in range(len(cardback_options)):
            choice_model = ConfigCardbackChoiceModel(rect=(0, 0, 0, 0), index=i,
                                                     config_manager=config_manager)
            choice_models.append(choice_model)
            pile.add(choice_model)

        pile_model = Model(elements=[pile_element])
        models = [pile_model] + choice_models
        super().__init__(models=models)
        return