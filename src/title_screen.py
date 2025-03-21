from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import ScaledText
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_title_screen(window_width, window_height, game_state):
    def new_game():
        game_state.set_value("play")
        return

    menu_items = [MenuItem(label="New Game", on_select=new_game)]
    menubar_model = MenuBar(rect=(0, 0, window_width, 25), menu_items=menu_items, max_menu_items=5)

    background_rectangle = Rectangle(rect=(0, 0, window_width, window_height), colour="lightgreen")
    title_text = ScaledText(rect=(window_width // 8, window_height // 6, 3 * window_width // 4, window_height // 2),
                            text="SOLITAIRE", colour="black", font_size=48, font_name="times", font_bold=True)
    static_model = Model(sprites=[background_rectangle, title_text])
    return ModelGroup(models=[static_model, menubar_model])


