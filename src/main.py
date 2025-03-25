from rich2d.game import Game, GameConfig
from rich2d.models.state import State, StateModel
from title_screen import solitaire_title_screen
from play_screen import solitaire_play_screen
from help_screen import solitaire_help_screen

window_width = 800
window_height = 600
game_config = GameConfig(window_width=window_width, window_height=window_height,
                         window_title="Solitaire", background_colour="darkgreen")
game_state = State(value="title")
title_model = solitaire_title_screen(game_state)
help_model = solitaire_help_screen(game_state)
play_model = solitaire_play_screen(game_state)

state_map = {'title': title_model, 'help': help_model, 'play': play_model}
game_model = StateModel(state=game_state, state_map=state_map)

solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()