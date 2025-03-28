from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import Text
from rich2d.models.ui import MenuBar, MenuItem
from models import ConfigBackgroundColourModel
from game import ConfigManager


def solitaire_config_screen(game_state, config_manager):
    def back():
        game_state.set_value("play")
        return

    menu_items = [MenuItem(label="Back", on_select=back)]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)

    background_colour_text_sprite = Text(rect=(50, 50, 700, 20), text="Background Colour",
                       colour="black", font_size=25, font_name="courier",
                       font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)

    background_colour_model_width = 100 + len(ConfigManager.background_colour_options()) * 50
    background_colour_model = ConfigBackgroundColourModel(rect=(50, 90, background_colour_model_width, 50),
                                                          config_manager=config_manager)

    background_rectangle = Rectangle(rect=(0, 0, 800, 600), colour="white")
    sprites = [background_rectangle, background_colour_text_sprite]
    static_model = Model(sprites=sprites)
    return ModelGroup(models=[static_model, menubar_model, background_colour_model])
