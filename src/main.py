from rich2d.game import Game, GameConfig
from rich2d.models import Model

window_width = 800
window_height = 600

game_config = GameConfig(window_width=window_width, window_height=window_height,
                         window_title="Solitaire", background_colour="darkgreen")
game_model = Model()
solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()
