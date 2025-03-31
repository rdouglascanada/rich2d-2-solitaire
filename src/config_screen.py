from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import Text
from rich2d.models.ui import MenuBar, MenuItem
from models import ConfigBackgroundColourModel, ConfigCardbackModel, ConfigCardsetModel
from game import ConfigManager


def solitaire_config_screen(game_state, config_manager):
    def back():
        game_state.set_value("play")
        return

    menu_items = [MenuItem(label="Back", on_select=back)]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)

    cardset_text_sprite = Text(rect=(50, 50, 700, 20), text="Card Set",
                               colour="black", font_size=25, font_name="courier",
                               font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    cardset_model = ConfigCardsetModel(rect=(30, 90, 740, 120), config_manager=config_manager)

    cardback_text_sprite = Text(rect=(50, 240, 700, 20), text="Card Back",
                                 colour="black", font_size=25, font_name="courier",
                                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    cardback_model = ConfigCardbackModel(rect=(30, 280, 740, 100), config_manager=config_manager)

    background_colour_text_sprite = Text(rect=(50, 420, 700, 20), text="Background Colour",
                       colour="black", font_size=25, font_name="courier",
                       font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)

    background_colour_model_width = 100 + len(ConfigManager.background_colour_options()) * 50
    background_colour_model = ConfigBackgroundColourModel(rect=(30, 460, background_colour_model_width, 50),
                                                          config_manager=config_manager)

    background_rectangle = Rectangle(rect=(0, 0, 800, 600), colour="white")
    sprites = [background_rectangle, cardset_text_sprite, cardback_text_sprite, background_colour_text_sprite]
    static_model = Model(sprites=sprites)
    return ModelGroup(models=[static_model, menubar_model, cardset_model, cardback_model, background_colour_model])
