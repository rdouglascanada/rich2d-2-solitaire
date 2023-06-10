from rich2d.game import Game, GameConfig
from rich2d.models import Model
from rich2d.sprites.images import ImageSprite
from card_image_sheet import CardImageSheet

window_width = 800
window_height = 600
game_config = GameConfig(window_width=window_width, window_height=window_height,
                         window_title="Solitaire", background_colour="darkgreen")

# card_images = CardImageSheet(file_name="resources/card_sheets/cutesy.png", image_width=80, image_height=120)
card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)
card_back_image = card_images.get_card_back_image()

deck_sprite = ImageSprite(image=card_back_image, rect=(30, 50, 80, 120))
king_of_hearts_image = card_images.get_card_image(rank=13, suit=CardImageSheet.Suit.HEARTS)
draw_sprite = ImageSprite(image=king_of_hearts_image, rect=(140, 50, 80, 120))

ace_of_spades_image = card_images.get_card_image(rank=1, suit=CardImageSheet.Suit.SPADES)
ace1_sprite = ImageSprite(image=ace_of_spades_image, rect=(360, 50, 80, 120))
ace_of_hearts_image = card_images.get_card_image(rank=1, suit=CardImageSheet.Suit.HEARTS)
ace2_sprite = ImageSprite(image=ace_of_hearts_image, rect=(470, 50, 80, 120))
ace_of_clubs_image = card_images.get_card_image(rank=1, suit=CardImageSheet.Suit.CLUBS)
ace3_sprite = ImageSprite(image=ace_of_clubs_image, rect=(580, 50, 80, 120))
ace_of_diamonds_image = card_images.get_card_image(rank=1, suit=CardImageSheet.Suit.DIAMONDS)
ace4_sprite = ImageSprite(image=ace_of_diamonds_image, rect=(690, 50, 80, 120))

queen_of_spades_image = card_images.get_card_image(rank=12, suit=CardImageSheet.Suit.SPADES)
klondike1_sprite = ImageSprite(image=queen_of_spades_image, rect=(30, 200, 80, 120))
klondike2_sprite = ImageSprite(image=card_back_image, rect=(140, 200, 80, 120))
klondike3_sprite = ImageSprite(image=card_back_image, rect=(250, 200, 80, 120))
klondike4_sprite = ImageSprite(image=card_back_image, rect=(360, 200, 80, 120))
klondike5_sprite = ImageSprite(image=card_back_image, rect=(470, 200, 80, 120))
klondike6_sprite = ImageSprite(image=card_back_image, rect=(580, 200, 80, 120))
klondike7_sprite = ImageSprite(image=card_back_image, rect=(690, 200, 80, 120))


sprites = [deck_sprite, draw_sprite,
           ace1_sprite, ace2_sprite, ace3_sprite, ace4_sprite,
           klondike1_sprite, klondike2_sprite, klondike3_sprite, klondike4_sprite,
           klondike5_sprite, klondike6_sprite, klondike7_sprite]

game_model = Model(sprites=sprites)
solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()
