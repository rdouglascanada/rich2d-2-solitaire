import pygame
from rich2d.game import exit_game
from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import Text
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_help_screen(window_width, window_height, game_state):
    def back():
        game_state.set_value("play")
        return

    menu_items = [MenuItem(label="Back", on_select=back)]
    menubar_model = MenuBar(rect=(0, 0, window_width, 25), menu_items=menu_items, max_menu_items=5)

    background_rectangle = Rectangle(rect=(0, 0, window_width, window_height), colour="white")
    line1 = Text(rect=(50, 50, 700, 20), text="Welcome to Solitaire!",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line2 = Text(rect=(50, 90, 700, 20), text="The object of the game is to get all of the cards into the four piles ",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line3 = Text(rect=(50, 120, 700, 20), text="in the top right of the playing area.",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line4 = Text(rect=(50, 160, 700, 20), text="Cards can be drawn by clicking on the deck in the top left.",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line5 = Text(rect=(50, 190, 700, 20), text="Cards are drawn into the pile next to the deck. If the deck is empty, ",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line6 = Text(rect=(50, 220, 700, 20), text="clicking will refill it with the contents of the draw pile.",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line7 = Text(rect=(50, 260, 700, 20), text="Cards can be moved by clicking on them, dragging them to",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line8 = Text(rect=(50, 290, 700, 20), text="their destination, and then releasing the mouse button.",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line9 = Text(rect=(50, 320, 700, 20), text="Only face-up cards are allowed to be moved.",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line10 = Text(rect=(50, 360, 700, 20), text="Cards in the four piles in the top right need to be in sequence",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line11 = Text(rect=(50, 390, 700, 20), text="from Ace to King for a given suit. Only Aces can be moved to",
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line12 = Text(rect=(50, 420, 700, 20), text="an empty pile. After that, it will be the next card in sequence.",
                  colour="black", font_size=25, font_name="calibri",
                  font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line13 = Text(rect=(50, 460, 700, 20), text="Faceup cards in the bottom piles follow a sequence of King to Ace.",
                  colour="black", font_size=25, font_name="calibri",
                  font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line14 = Text(rect=(50, 490, 700, 20), text="Here the suit is not the same but needs to alternate in colour.",
                  colour="black", font_size=25, font_name="calibri",
                  font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line15 = Text(rect=(50, 520, 700, 20), text="Facedown cards are turned faceup when the faceup card in front",
                  colour="black", font_size=25, font_name="calibri",
                  font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    line16 = Text(rect=(50, 550, 700, 20), text="is moved. Multiple cards may be moved at the same time.",
                  colour="black", font_size=25, font_name="calibri",
                  font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
    sprites = [background_rectangle, line1, line2, line3, line4,
               line5, line6, line7, line8, line9, line10, line11,
               line12, line13, line14, line15, line16]
    static_model = Model(sprites=sprites)
    return ModelGroup(models=[static_model, menubar_model])


