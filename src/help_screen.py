import pygame
from rich2d.game import exit_game
from rich2d.models import Model, ModelGroup
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.text import Text
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_help_screen(game_state):
    def back():
        game_state.set_value("play")
        return

    menu_items = [MenuItem(label="Back", on_select=back)]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)

    background_rectangle = Rectangle(rect=(0, 0, 800, 600), colour="white")
    lines = {
        'text_sprites': [],
        'next_line_y': 0
    }

    def add_line(text, vertical_displacement):
        lines['next_line_y'] += vertical_displacement
        text_sprite = Text(rect=(50, lines['next_line_y'], 700, 20), text=text,
                 colour="black", font_size=25, font_name="calibri",
                 font_bold=True, horizontal_alignment=Text.HorizontalAlignment.LEFT)
        lines['text_sprites'].append(text_sprite)
        return

    add_line("Welcome to Solitaire!", 50)
    add_line("The object of the game is to get all of the cards into the four piles ", 40)
    add_line("in the top right of the playing area.", 30)
    add_line("Cards can be drawn by clicking on the deck in the top left.", 40)
    add_line("Cards are drawn into the pile next to the deck. If the deck is empty, ", 30)
    add_line("clicking will refill it with the contents of the draw pile.", 30)
    add_line("Cards can be moved by clicking on them, dragging them to", 40)
    add_line("their destination, and then releasing the mouse button.", 30)
    add_line("Only face-up cards are allowed to be moved.", 30)
    add_line("Cards in the four piles in the top right need to be in sequence", 40)
    add_line("from Ace to King for a given suit. Only Aces can be moved to", 30)
    add_line("an empty pile. After that, it will be the next card in sequence.", 30)
    add_line("Faceup cards in the bottom piles follow a sequence of King to Ace.", 40)
    add_line("Here the suit is not the same but needs to alternate in colour.", 30)
    add_line("Facedown cards are turned faceup when the faceup card in front", 30)
    add_line("is moved. Multiple cards may be moved at the same time.", 30)

    sprites = [background_rectangle] + lines['text_sprites']
    static_model = Model(sprites=sprites)
    return ModelGroup(models=[static_model, menubar_model])


