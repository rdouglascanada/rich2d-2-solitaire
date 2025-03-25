from rich2d.game import exit_game
from rich2d.models import ModelGroup
from rich2d.sprites.images import Image
from game import Deck, UndoStack, CardCollection, DeckManager
from sprites import CardImageSheet
from models import SelectionModel, DeckCollectionModel, DrawCollectionModel,\
    SuitCollectionModel, KlondikeCardCollectionModel
from rich2d.models.ui import MenuBar, MenuItem


def solitaire_play_screen(game_state):
    card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)
    deck_collection_background_image = Image.load_from_file("resources/deck_background.png")
    card_collection_background_image = Image.load_from_file("resources/empty_collection.png")
    undo_stack = UndoStack()

    deck = Deck()
    deck_card_collection = CardCollection()
    draw_card_collection = CardCollection()
    deck_manager = DeckManager(deck_card_collection=deck_card_collection,
                               draw_card_collection=draw_card_collection,
                               undo_stack=undo_stack)
    selection_model = SelectionModel(card_image_sheet=card_images)

    draw_collection_model = DrawCollectionModel(rect=(140, 50, 80, 120),
                                                selection_model=selection_model,
                                                card_image_sheet=card_images,
                                                draw_card_collection=draw_card_collection)
    deck_collection_model = DeckCollectionModel(rect=(30, 50, 80, 120),
                                                selection_model=selection_model,
                                                card_image_sheet=card_images,
                                                background_image=deck_collection_background_image,
                                                deck_card_collection=deck_card_collection,
                                                deck_manager=deck_manager)

    suit_collection_models = []
    suit_collection_rects = [(360, 50, 80, 120), (470, 50, 80, 120), (580, 50, 80, 120), (690, 50, 80, 120)]
    for suit_collection_rect in suit_collection_rects:
        suit_collection_models.append(SuitCollectionModel(rect=suit_collection_rect,
                                                          selection_model=selection_model,
                                                          card_image_sheet=card_images,
                                                          background_image=card_collection_background_image,
                                                          undo_stack=undo_stack))

    klondike_pile_models = []
    klondike_pile_rects = [(30, 200, 80, 120), (140, 200, 80, 120), (250, 200, 80, 120),
                           (360, 200, 80, 120), (470, 200, 80, 120), (580, 200, 80, 120),
                           (690, 200, 80, 120)]
    for klondike_pile_rect in klondike_pile_rects:
        klondike_pile_models.append(KlondikeCardCollectionModel(rect=klondike_pile_rect,
                                                                selection_model=selection_model,
                                                                card_image_sheet=card_images,
                                                                background_image=card_collection_background_image,
                                                                undo_stack=undo_stack))

    def new_game():
        for pile_model in klondike_pile_models + suit_collection_models + [deck_collection_model, draw_collection_model]:
            pile_model.remove_all()
        undo_stack.remove_all()
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

    def undo():
        undo_stack.undo()
        return

    def view_help():
        game_state.set_value("help")
        return

    def quit_game():
        exit_game()
        return

    menu_items = [
        MenuItem(label="New Game", on_select=new_game),
        MenuItem(label="Undo", on_select=undo),
        MenuItem(label="Help", on_select=view_help),
        MenuItem(label="Quit Game", on_select=quit_game)
    ]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)
    models = klondike_pile_models + suit_collection_models + [menubar_model, deck_collection_model, draw_collection_model,
                                                              selection_model]
    new_game()
    return ModelGroup(models=models)

