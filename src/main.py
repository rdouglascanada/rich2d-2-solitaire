from rich2d.game import Game, GameConfig
from rich2d.models import Model, ModelGroup
from rich2d.handlers import MouseHandler
from rich2d.sprites.images import Image
from cards import Deck, CardCollection
from sprites import CardImageSheet, CardCollectionSprite, CardCollectionBackgroundSprite
from models import SelectionModel, SuitCollectionModel, KlondikePileModel

window_width = 800
window_height = 600
game_config = GameConfig(window_width=window_width, window_height=window_height,
                         window_title="Solitaire", background_colour="darkgreen")

card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)

deck_collection_background_image = Image.load_from_file("resources/deck_background.png")
card_collection_background_image = Image.load_from_file("resources/empty_collection.png")

deck = Deck()
deck.shuffle()

deck_collection = CardCollection(cards=deck.get_cards())
deck_collection_sprite = CardCollectionSprite(card_collection=deck_collection, card_image_sheet=card_images,
                                              rect=(30, 50, 80, 120), shown=False)
deck_collection_background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=deck_collection_sprite,
                                                                   background_image=deck_collection_background_image)
draw_collection = CardCollection(cards=[])
draw_collection_sprite = CardCollectionSprite(card_collection=draw_collection, card_image_sheet=card_images,
                                              rect=(140, 50, 80, 120), shown=True)

selection_model = SelectionModel(card_image_sheet=card_images)

suit_collection_models = []
suit_collection_rects = [(360, 50, 80, 120), (470, 50, 80, 120), (580, 50, 80, 120), (690, 50, 80, 120)]
for suit_collection_rect in suit_collection_rects:
    suit_collection_models.append(SuitCollectionModel(rect=suit_collection_rect,
                                                      selection_model=selection_model,
                                                      card_image_sheet=card_images,
                                                      background_image=card_collection_background_image))

klondike_pile_models = []
klondike_pile_rects = [(30, 200, 80, 120), (140, 200, 80, 120), (250, 200, 80, 120),
                       (360, 200, 80, 120), (470, 200, 80, 120), (580, 200, 80, 120),
                       (690, 200, 80, 120)]
klondike_background_sprites = []
for klondike_pile_rect in klondike_pile_rects:
    klondike_pile_models.append(KlondikePileModel(rect=klondike_pile_rect,
                                                  selection_model=selection_model,
                                                  card_image_sheet=card_images,
                                                  background_image=card_collection_background_image))


def on_draw_collection_click():
    if selection_model.is_empty():
        card_collection = draw_collection_sprite.get_card_collection()
        if not card_collection.is_empty():
            card = card_collection.draw()
            selection_model.add_card(card, shown=True)
            selection_model.set_last_selected_collection(card_collection)
    return


def draw_card():
    if not deck_collection.is_empty():
        draw_collection.insert(deck_collection.draw())
    else:
        while not draw_collection.is_empty():
            deck_collection.insert(draw_collection.draw())
    return


deck_collection_handler = MouseHandler(rect=deck_collection_sprite.get_rect(),
                                       on_left_mouse_click=draw_card)
draw_collection_handler = MouseHandler(rect=draw_collection_sprite.get_rect(),
                                       on_left_mouse_click=on_draw_collection_click)


sprites = [deck_collection_background_sprite, deck_collection_sprite, draw_collection_sprite]
handlers = [deck_collection_handler, draw_collection_handler]

game_model = ModelGroup(models=klondike_pile_models + suit_collection_models +
                               [Model(sprites=sprites, handlers=handlers), selection_model])
solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()
