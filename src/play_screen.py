from rich2d.game import exit_game
from rich2d.models import ModelGroup
from rich2d.sprites.images import Image
from cards import Deck
from sprites import CardImageSheet
from models import SelectionModel, DeckCollectionModel, DrawCollectionModel,\
    SuitCollectionModel, KlondikeCardCollectionModel
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_play_screen(window_width):
    card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)
    deck_collection_background_image = Image.load_from_file("resources/deck_background.png")
    card_collection_background_image = Image.load_from_file("resources/empty_collection.png")

    selection_model = SelectionModel(card_image_sheet=card_images)

    draw_collection_model = DrawCollectionModel(rect=(140, 50, 80, 120),
                                                selection_model=selection_model,
                                                card_image_sheet=card_images)
    deck_collection_model = DeckCollectionModel(rect=(30, 50, 80, 120),
                                                selection_model=selection_model,
                                                card_image_sheet=card_images,
                                                background_image=deck_collection_background_image,
                                                draw_collection_model=draw_collection_model)

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
    for klondike_pile_rect in klondike_pile_rects:
        klondike_pile_models.append(KlondikeCardCollectionModel(rect=klondike_pile_rect,
                                                                selection_model=selection_model,
                                                                card_image_sheet=card_images,
                                                                background_image=card_collection_background_image))

    def new_game():
        for pile_model in klondike_pile_models + suit_collection_models + [deck_collection_model, draw_collection_model]:
            pile_model.remove_all()

        deck = Deck()
        deck.shuffle()
        cards = deck.get_cards()
        c = 0

        for i in range(len(klondike_pile_models)):
            klondike_pile_model = klondike_pile_models[i]
            klondike_card_collection = klondike_pile_model.get_card_collection()
            for j in range(i + 1):
                klondike_card_collection.insert(cards[c])
                c += 1
            klondike_pile_model.hide_all_but_last()

        deck_card_collection = deck_collection_model.get_card_collection()
        for card in cards[c:]:
            deck_card_collection.insert(card)
        return

    def quit_game():
        exit_game()
        return

    new_game()
    menu_items = [MenuItem(label="New Game", on_select=new_game), MenuItem(label="Quit Game", on_select=quit_game)]
    menubar_model = MenuBar(rect=(0, 0, window_width, 25), menu_items=menu_items, max_menu_items=5)
    models = klondike_pile_models + suit_collection_models + [menubar_model, deck_collection_model, draw_collection_model,
                                                              selection_model]
    return ModelGroup(models=models)

