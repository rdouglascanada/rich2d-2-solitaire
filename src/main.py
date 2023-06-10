from rich2d.game import Game, GameConfig
from rich2d.models import Model
from rich2d.sprites.images import ImageSprite
from card import Card
from card_sprite import CardSprite
from card_image_sheet import CardImageSheet

window_width = 800
window_height = 600
game_config = GameConfig(window_width=window_width, window_height=window_height,
                         window_title="Solitaire", background_colour="darkgreen")

card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)

deck_sprite = CardSprite(card=Card(rank=2, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                         rect=(30, 50, 80, 120), shown=False)
draw_sprite = CardSprite(card=Card(rank=13, suit=Card.Suit.HEARTS), card_image_sheet=card_images,
                         rect=(140, 50, 80, 120), shown=True)

ace1_sprite = CardSprite(card=Card(rank=1, suit=Card.Suit.SPADES), card_image_sheet=card_images,
                         rect=(360, 50, 80, 120), shown=True)
ace2_sprite = CardSprite(card=Card(rank=1, suit=Card.Suit.HEARTS), card_image_sheet=card_images,
                         rect=(470, 50, 80, 120), shown=True)
ace3_sprite = CardSprite(card=Card(rank=1, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                         rect=(580, 50, 80, 120), shown=True)
ace4_sprite = CardSprite(card=Card(rank=1, suit=Card.Suit.DIAMONDS), card_image_sheet=card_images,
                         rect=(690, 50, 80, 120), shown=True)

klondike1_sprite = CardSprite(card=Card(rank=12, suit=Card.Suit.SPADES), card_image_sheet=card_images,
                              rect=(30, 200, 80, 120), shown=True)
klondike2_sprite = CardSprite(card=Card(rank=3, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(140, 200, 80, 120), shown=False)
klondike3_sprite = CardSprite(card=Card(rank=4, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(250, 200, 80, 120), shown=False)
klondike4_sprite = CardSprite(card=Card(rank=5, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(360, 200, 80, 120), shown=False)
klondike5_sprite = CardSprite(card=Card(rank=6, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(470, 200, 80, 120), shown=False)
klondike6_sprite = CardSprite(card=Card(rank=7, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(580, 200, 80, 120), shown=False)
klondike7_sprite = CardSprite(card=Card(rank=8, suit=Card.Suit.CLUBS), card_image_sheet=card_images,
                              rect=(690, 200, 80, 120), shown=False)


sprites = [deck_sprite, draw_sprite,
           ace1_sprite, ace2_sprite, ace3_sprite, ace4_sprite,
           klondike1_sprite, klondike2_sprite, klondike3_sprite, klondike4_sprite,
           klondike5_sprite, klondike6_sprite, klondike7_sprite]

game_model = Model(sprites=sprites)
solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()
