from rich2d.game import exit_game
from rich2d.models import Model, ModelGroup
from rich2d.models.ui import MenuBar, MenuItem
from rich2d.elements import Element
from rich2d.sprites.shapes import Rectangle
from rich2d.sprites.images import Image
from game import GameManager
from sprites import CardImageSheet
from models import SelectionModel, DeckCollectionModel, DrawCollectionModel,\
    SuitCollectionModel, KlondikeCollectionModel, YouWinModel


def solitaire_play_screen(game_state, config_manager):
    card_images = CardImageSheet(file_name="resources/card_sheets/old_windows.png", image_width=71, image_height=96)
    deck_collection_background_image = Image.load_from_file("resources/deck_background.png")
    card_collection_background_image = Image.load_from_file("resources/empty_collection.png")

    game_manager = GameManager()

    selection_model = SelectionModel(card_image_sheet=card_images,
                                     selection_manager=game_manager.get_selection_manager())
    deck_collection_model = DeckCollectionModel(rect=(30, 50, 80, 120),
                                                card_image_sheet=card_images,
                                                background_image=deck_collection_background_image,
                                                deck_draw_manager=game_manager.get_deck_draw_manager())
    draw_collection_model = DrawCollectionModel(rect=(140, 50, 80, 120),
                                                selection_manager=game_manager.get_selection_manager(),
                                                card_image_sheet=card_images,
                                                deck_draw_manager=game_manager.get_deck_draw_manager())


    suit_collection_models = []
    suit_card_collections = game_manager.get_suit_card_collections()
    suit_collection_rects = [(360, 50, 80, 120), (470, 50, 80, 120), (580, 50, 80, 120), (690, 50, 80, 120)]
    for i in range(len(suit_card_collections)):
        suit_card_collection = suit_card_collections[i]
        rect = suit_collection_rects[i]
        suit_collection_models.append(SuitCollectionModel(suit_card_collection=suit_card_collection,
                                                          rect=rect,
                                                          selection_manager=game_manager.get_selection_manager(),
                                                          card_image_sheet=card_images,
                                                          background_image=card_collection_background_image,
                                                          undo_stack=game_manager.get_undo_stack()))

    klondike_pile_models = []
    klondike_card_collections = game_manager.get_klondike_card_collections()
    klondike_pile_rects = [(30, 200, 80, 120), (140, 200, 80, 120), (250, 200, 80, 120),
                           (360, 200, 80, 120), (470, 200, 80, 120), (580, 200, 80, 120),
                           (690, 200, 80, 120)]
    for i in range(len(klondike_card_collections)):
        klondike_card_collection = klondike_card_collections[i]
        rect = klondike_pile_rects[i]
        klondike_pile_models.append(KlondikeCollectionModel(klondike_card_collection=klondike_card_collection,
                                                            rect=rect,
                                                            selection_manager=game_manager.get_selection_manager(),
                                                            card_image_sheet=card_images,
                                                            background_image=card_collection_background_image,
                                                            undo_stack=game_manager.get_undo_stack()))

    you_win_model = YouWinModel(rect=(30, 200, 740, 370), game_manager=game_manager)

    def new_game():
        game_manager.new_game()
        for klondike_pile_model in klondike_pile_models:
            klondike_pile_model.refresh()
        return

    def undo():
        undo_stack = game_manager.get_undo_stack()
        undo_stack.undo()
        return

    def view_help():
        game_state.set_value("help")
        return

    def configure_game():
        game_state.set_value("config")
        return

    def quit_game():
        exit_game()
        return

    menu_items = [
        MenuItem(label="New Game", on_select=new_game),
        MenuItem(label="Undo", on_select=undo),
        MenuItem(label="Help", on_select=view_help),
        MenuItem(label="Config", on_select=configure_game),
        MenuItem(label="Quit Game", on_select=quit_game)
    ]
    menubar_model = MenuBar(rect=(0, 0, 800, 25), menu_items=menu_items, max_menu_items=5)

    background_rectangle = Rectangle(rect=(0, 0, 800, 600))
    def sync_background_colour():
        background_rectangle.set_colour(colour=config_manager.get_background_colour())
        return
    sync_background_element = Element(on_update=sync_background_colour)
    background_model = Model(sprites=[background_rectangle], elements=[sync_background_element])

    models = [background_model, menubar_model, deck_collection_model, draw_collection_model] + \
              klondike_pile_models + suit_collection_models + [you_win_model, selection_model]
    new_game()
    return ModelGroup(models=models)

