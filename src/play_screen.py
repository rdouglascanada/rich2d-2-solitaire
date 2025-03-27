from rich2d.game import exit_game
from rich2d.models import ModelGroup
from rich2d.models.ui import MenuBar, MenuItem
from rich2d.sprites.images import Image
from game import Deck, CardCollection, UndoStack, DeckDrawManager, SelectionManager
from sprites import CardImageSheet
from models import SelectionModel, DeckCollectionModel, DrawCollectionModel,\
    SuitCollectionModel, KlondikeCollectionModel


def solitaire_play_screen(game_state):
    card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)
    deck_collection_background_image = Image.load_from_file("resources/deck_background.png")
    card_collection_background_image = Image.load_from_file("resources/empty_collection.png")

    deck = Deck()
    undo_stack = UndoStack()
    selection_manager = SelectionManager()
    deck_draw_manager = DeckDrawManager(undo_stack=undo_stack)

    selection_model = SelectionModel(card_image_sheet=card_images, selection_manager=selection_manager)
    deck_collection_model = DeckCollectionModel(rect=(30, 50, 80, 120),
                                                card_image_sheet=card_images,
                                                background_image=deck_collection_background_image,
                                                deck_draw_manager=deck_draw_manager)
    draw_collection_model = DrawCollectionModel(rect=(140, 50, 80, 120),
                                                selection_manager=selection_manager,
                                                card_image_sheet=card_images,
                                                deck_draw_manager=deck_draw_manager)


    suit_collection_models = []
    suit_card_collections = [CardCollection(), CardCollection(), CardCollection(), CardCollection()]
    suit_collection_rects = [(360, 50, 80, 120), (470, 50, 80, 120), (580, 50, 80, 120), (690, 50, 80, 120)]
    for i in range(len(suit_card_collections)):
        suit_card_collection = suit_card_collections[i]
        rect = suit_collection_rects[i]
        suit_collection_models.append(SuitCollectionModel(suit_card_collection=suit_card_collection,
                                                          rect=rect,
                                                          selection_manager=selection_manager,
                                                          card_image_sheet=card_images,
                                                          background_image=card_collection_background_image,
                                                          undo_stack=undo_stack))

    klondike_pile_models = []
    klondike_card_collections = [CardCollection(), CardCollection(), CardCollection(),
                                 CardCollection(), CardCollection(), CardCollection(),
                                 CardCollection()]
    klondike_pile_rects = [(30, 200, 80, 120), (140, 200, 80, 120), (250, 200, 80, 120),
                           (360, 200, 80, 120), (470, 200, 80, 120), (580, 200, 80, 120),
                           (690, 200, 80, 120)]
    for i in range(len(klondike_card_collections)):
        klondike_card_collection = klondike_card_collections[i]
        rect = klondike_pile_rects[i]
        klondike_pile_models.append(KlondikeCollectionModel(klondike_card_collection=klondike_card_collection,
                                                            rect=rect,
                                                            selection_manager=selection_manager,
                                                            card_image_sheet=card_images,
                                                            background_image=card_collection_background_image,
                                                            undo_stack=undo_stack))

    def new_game():
        card_collections = [deck_draw_manager.get_deck_card_collection(),
                            deck_draw_manager.get_draw_card_collection(),
                            selection_manager.get_card_collection()] + \
            suit_card_collections + klondike_card_collections
        for card_collection in card_collections:
            card_collection.remove_all()
        undo_stack.remove_all()
        deck.shuffle()
        cards = deck.get_cards()
        deck_card_collection = deck_draw_manager.get_deck_card_collection()

        c = 0
        for i in range(len(klondike_card_collections)):
            card_collection = klondike_card_collections[i]
            for j in range(i + 1):
                cards[c].hide()
                card_collection.insert(cards[c])
                c += 1
            cards[c - 1].show()

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

