import pygame
from rich2d.game import exit_game
from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import ScaledText
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_title_screen(game_state):
    def new_game():
        game_state.set_value("play")
        return

    def quit_game():
        exit_game()
        return

    menu_items = [MenuItem(label="New Game", on_select=new_game), MenuItem(label="Quit Game", on_select=quit_game)]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)

    background_rectangle = Rectangle(rect=(0, 0, 800, 600), colour="darkgreen")
    title_text = ScaledText(rect=(100, 100, 600, 300),
                            text="SOLITAIRE", colour="black", font_size=48, font_name="times", font_bold=True)
    static_model = Model(sprites=[background_rectangle, title_text])
    return ModelGroup(models=[static_model, menubar_model])


