from rich2d.game import Game, GameConfig
from rich2d.models import Model, ModelGroup
from rich2d.handlers import MouseHandler
from rich2d.sprites.images import Image
from cards import Card, Deck, CardCollection
from sprites import CardSprite, CardImageSheet, CardCollectionSprite, CardCollectionBackgroundSprite
from selection_model import SelectionModel

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

suit1_collection = CardCollection()
suit1_collection_sprite = CardCollectionSprite(card_collection=suit1_collection, card_image_sheet=card_images,
                                               rect=(360, 50, 80, 120), shown=True)
suit1_collection_background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=suit1_collection_sprite,
                                                                    background_image=card_collection_background_image)
suit2_collection = CardCollection()
suit2_collection_sprite = CardCollectionSprite(card_collection=suit2_collection, card_image_sheet=card_images,
                                               rect=(470, 50, 80, 120), shown=True)
suit2_collection_background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=suit2_collection_sprite,
                                                                    background_image=card_collection_background_image)
suit3_collection = CardCollection()
suit3_collection_sprite = CardCollectionSprite(card_collection=suit3_collection, card_image_sheet=card_images,
                                               rect=(580, 50, 80, 120), shown=True)
suit3_collection_background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=suit3_collection_sprite,
                                                                    background_image=card_collection_background_image)
suit4_collection = CardCollection()
suit4_collection_sprite = CardCollectionSprite(card_collection=suit4_collection, card_image_sheet=card_images,
                                               rect=(690, 50, 80, 120), shown=True)
suit4_collection_background_sprite = CardCollectionBackgroundSprite(card_collection_sprite=suit4_collection_sprite,
                                                                    background_image=card_collection_background_image)

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

selection_model = SelectionModel(card_image_sheet=card_images)


def on_draw_collection_click():
    if selection_model.is_empty():
        card_collection = draw_collection_sprite.get_card_collection()
        if not card_collection.is_empty():
            card = card_collection.draw()
            selection_model.add_card(card, shown=True)
            selection_model.set_last_selected_collection(card_collection)
    return


def suit_collection_handler(suit_collection_sprite):
    def on_click():
        if selection_model.is_empty():
            card_collection = suit_collection_sprite.get_card_collection()
            if not card_collection.is_empty():
                card = card_collection.draw()
                selection_model.add_card(card, shown=True)
                selection_model.set_last_selected_collection(card_collection)
        return

    def on_release():
        if selection_model.is_empty():
            return
        if len(selection_model) > 1:
            undo_selection()
        selected_card = selection_model.remove_all()[0]
        suit_collection = suit_collection_sprite.get_card_collection()
        last_selected_collection = selection_model.get_last_selected_collection()

        if suit_collection.is_empty() and selected_card.get_rank() != 1:
            last_selected_collection.insert(selected_card)
        elif suit_collection.is_empty():
            suit_collection.insert(selected_card)
        else:
            top_card = suit_collection.peek()
            correct_suit = top_card.get_suit() == selected_card.get_suit()
            correct_rank = top_card.get_rank() + 1 == selected_card.get_rank()
            if correct_rank and correct_suit:
                suit_collection.insert(selected_card)
            else:
                last_selected_collection.insert(selected_card)
        return

    return MouseHandler(rect=suit_collection_sprite.get_rect(),
                        on_left_mouse_click=on_click,
                        on_left_mouse_release=on_release)


def undo_selection():
    if selection_model.is_empty():
        return
    selected_cards = selection_model.remove_all()
    last_selected_collection = selection_model.get_last_selected_collection()
    for card in selected_cards:
        last_selected_collection.insert(card)
    return


def draw_card():
    if not deck_collection.is_empty():
        draw_collection.insert(deck_collection.draw())
    else:
        while not draw_collection.is_empty():
            deck_collection.insert(draw_collection.draw())
    return


default_on_release_handler = MouseHandler(on_left_mouse_release=undo_selection)
deck_collection_handler = MouseHandler(rect=deck_collection_sprite.get_rect(),
                                       on_left_mouse_click=draw_card)
draw_collection_handler = MouseHandler(rect=draw_collection_sprite.get_rect(),
                                       on_left_mouse_click=on_draw_collection_click)
suit_collection_handlers = [suit_collection_handler(suit_collection_sprite)
                            for suit_collection_sprite in
                            [suit1_collection_sprite, suit2_collection_sprite,
                             suit3_collection_sprite, suit4_collection_sprite]]


sprites = [deck_collection_background_sprite, deck_collection_sprite, draw_collection_sprite,
           suit1_collection_background_sprite, suit2_collection_background_sprite,
           suit3_collection_background_sprite, suit4_collection_background_sprite,
           suit1_collection_sprite, suit2_collection_sprite, suit3_collection_sprite, suit4_collection_sprite,
           klondike1_sprite, klondike2_sprite, klondike3_sprite, klondike4_sprite,
           klondike5_sprite, klondike6_sprite, klondike7_sprite]
handlers = suit_collection_handlers + [deck_collection_handler, draw_collection_handler, default_on_release_handler]

game_model = ModelGroup(models=[Model(sprites=sprites, handlers=handlers), selection_model])
solitaire_game = Game(model=game_model, config=game_config)
solitaire_game.run()
