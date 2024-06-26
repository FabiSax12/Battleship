import sys
import tkinter                  as tk
import tk_logic.custom_widgets  as custom
from enums                      import Color, GameStage
from game_logic.board           import clean_board
from game_logic.ships           import print_all_ships
from game_data                  import game_data, find_saved_games, save_game_data
from game_logic.config          import set_game_config

players = game_data["players"]

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

def center_window(window_width: int, window_height: int) -> list:
    """
    Calculate the coordinates to center a window on the screen.

    Args:
        window_width: The width of the window.
        window_height: The height of the window.

    Returns:
        list: A list containing the x and y coordinates to center the window.
    """
    pos_x = screen_width // 2 - window_width // 2
    pos_y = screen_height // 2 - window_height // 2

    return [pos_x, pos_y]

def center_widget(widget: tk.Widget, window_width: int, window_height: int, x=None, y=None, w_divider=2, h_divider=2, x_fraction=1, y_fraction=1) -> list:
    """
    Center a widget within a window.

    Args:
        widget: The widget to be centered.
        window_width: The width of the window.
        window_height: The height of the window.
        x: The x-coordinate of the widget's top-left corner (optional).
        y: The y-coordinate of the widget's top-left corner (optional).
        w_divider: The divider for the width (optional, default is 2).
        h_divider: The divider for the height (optional, default is 2).
        x_fraction: The fraction of the window's width for x-coordinate calculation (optional, default is 1).
        y_fraction: The fraction of the window's height for y-coordinate calculation (optional, default is 1).

    Returns:
        list: A list containing the x and y coordinates of the widget's top-left corner.
    """
    widget_width = widget.winfo_reqwidth()
    widget_height = widget.winfo_reqheight()

    new_x = x if x is not None else window_width // w_divider * x_fraction - widget_width // 2
    new_y = y if y is not None else window_height // h_divider * y_fraction - widget_height // 2

    widget.place_configure(x=new_x, y=new_y)

def create_player_info_frame(window: tk.Tk, player: int):
    player_info = game_data["players"][player]
    player_ships = game_data["board_1_ships" if player == 0 else "board_2_ships"]
    board = game_data["board_1" if player == 0 else "board_2"]

    player_info_frame = custom.Div(window)
    player_info_frame.title(player_info["nickname"])
    player_info_frame.config(width=game_data["board_columns"] // 2 * game_data["button_width"] // 2, height=screen_height // 4)

    points_label = custom.Label(player_info_frame, text=f"Puntos: {player_info['points']}")
    points_label.pack(anchor="w")

    destructor_label = custom.Label(player_info_frame, text=f"Destructores: {player_info['ships']['destructor']}")
    destructor_label.pack(anchor="w")

    crucero_label = custom.Label(player_info_frame, text=f"Cruceros: {player_info['ships']['crucero']}")
    crucero_label.pack(anchor="w")

    acorazado_label = custom.Label(player_info_frame, text=f"Acorazados: {player_info['ships']['acorazado']}")
    acorazado_label.pack(anchor="w")

    def hide():
        show_ships_button.config(text="Mostrar barcos", command=show, bg=Color.BLACK.value)
        clean_board(board)


    def show():
        show_ships_button.config(text="Ocultar barcos", command=hide, bg=Color.GRAY.value)
        print_all_ships(player_ships, board)

    show_ships_button = custom.Button(player_info_frame, "Mostrar barcos", show)

    if game_data["game_stage"] == GameStage.PLAYING:
        show_ships_button.config(state=tk.NORMAL if player + 1 == game_data["turn"] else tk.DISABLED)
        show_ships_button.pack(side=tk.BOTTOM, pady=10, expand=True, fill=tk.X)

    player_info_frame.place(x=0, y=0)

    return player_info_frame

def update_player_info_frame(player_info_frame, player: int):
    player_info = game_data["players"][player]
    frame_children = player_info_frame.winfo_children()[0].winfo_children()

    points_label = frame_children[1]
    destructor_label = frame_children[2]
    crucero_label = frame_children[3]
    acorazado_label = frame_children[4]
    button = frame_children[5]

    points_label.config(text=f"Puntos: {player_info['points']}")
    destructor_label.config(text=f"Destructores: {player_info['ships']['destructor']}")
    crucero_label.config(text=f"Cruceros: {player_info['ships']['crucero']}")
    acorazado_label.config(text=f"Acorazados: {player_info['ships']['acorazado']}")

    if game_data["game_stage"] == GameStage.PLAYING:
        button.config(state=tk.NORMAL if player + 1 == game_data["turn"] else tk.DISABLED)
        button.pack(side=tk.BOTTOM, pady=10, expand=True, fill=tk.X)

def list_of_saved_games(parent_window, title, action) -> custom.Div:
    """
    Create a list of saved games.

    Args:
        parent_window: The parent window to contain the list.
        title: The title of the list.
        action: The action to perform on double-click.

    Returns:
        custom.Div: The frame containing the list of saved games.
    """
    saved_games = custom.Div(parent_window)
    saved_games.title(title)
    
    scrollbar = custom.Scrollbar(saved_games)
    listbox = custom.Listbox(saved_games, yscrollcommand=scrollbar.set)
    
    scrollbar.axis("y")
    scrollbar.config(command=listbox.yview)
    
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox.double_click(action, destroy=True)

    find_saved_games()
    for file_name in game_data["saved_games"]:
        listbox.insert(tk.END, file_name)

    return saved_games

def create_load_game_screen(window: tk.Tk, start_old_game) -> tk.Tk:
    """
    Create the load game screen.

    Args:
        window (tk.Tk): The parent window to destroy.
        start_old_game: The function to start an old game.

    Returns:
        tk.Tk: The load game screen window.
    """
    window.destroy()

    window_load_game = tk.Tk()
    window_load_game.title("Cargar partida")

    window_width = screen_width // 4
    window_height = screen_height // 2

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_load_game.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_load_game.resizable(0, 0)

    saved_games_list = list_of_saved_games(window_load_game, "Partidas Guardadas", start_old_game)
    saved_games_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=50, pady=50)
    
    return window_load_game

def create_save_game_screen() -> tk.Tk:
    """
    Create the save game screen.

    Returns:
        tk.Tk: The save game screen window.
    """
    window_save_game = tk.Tk()
    window_save_game.title("Guardar Partida")
    
    window_width = screen_width // 4
    window_height = screen_height // 2

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_save_game.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_save_game.resizable(0, 0)

    save_game_label = custom.Label(window_save_game, "Nombre de la partida:")
    center_widget(save_game_label, window_width, window_height, y=window_height // 10)

    save_game_entry = custom.Entry(window_save_game)
    center_widget(save_game_entry, window_width, window_height, y=window_height // 10 + 50)

    def on_click():
        save_game_data(save_game_entry.get())
        window_save_game.destroy()

    save_game_button = custom.Button(window_save_game, "Guardar", on_click)
    center_widget(save_game_button, window_width, window_height, y=window_height // 10 + 100)

    saved_games_list = list_of_saved_games(window_save_game, "Sobreescribir partida guardada", save_game_data)
    # saved_games_list.config(height=window_height // 2, width=window_width)
    # saved_games_list.place(x=0, y=window_height // 2)
    saved_games_list.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(window_height // 2, 0))

    return window_save_game

def create_game_screen() -> tk.Tk:
    """
    Create the main game screen.

    Returns:
        tk.Tk: The main game screen window.
    """
    game_screen = tk.Tk()
    game_screen.title("Battleship")
    game_screen.protocol("WM_DELETE_WINDOW", sys.exit)
    game_screen.state("zoomed")
    custom.Button(game_screen, "Guardar", lambda: create_save_game_screen().mainloop()).place(x=0, y=0)
    
    return game_screen

def create_new_game_screen() -> tk.Tk:
    """
    Create the screen for setting up a new game.

    Returns:
        tk.Tk: The new game setup window.
    """
    window_player_form = tk.Tk()

    window_player_form.title("Menu")
    
    window_width = int(screen_width // 2)
    window_height = int(screen_height // 2)

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_player_form.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_player_form.resizable(0,0)
    
    game_log = custom.Label(window_player_form, "Registro de jugadores", 17)
    center_widget(game_log, window_width, window_height, y=20)
    
    player1 = custom.Label(window_player_form, "Jugador 1:")
    center_widget(player1, window_width, window_height, y=100, w_divider=4, x_fraction=1)
    player_name1 = custom.Entry(window_player_form)
    center_widget(player_name1, window_width, window_height, y=150, w_divider=4, x_fraction=1)

    player2 = custom.Label(window_player_form, "Jugador 2:")
    center_widget(player2, window_width, window_height, y=100, w_divider=4, x_fraction=3)
    player_name2 = custom.Entry(window_player_form)
    center_widget(player_name2, window_width, window_height, y=150, w_divider=4, x_fraction=3)
    
    game_settings = custom.Label(window_player_form, "Tablero", 17)
    center_widget(game_settings, window_width, window_height, y=200)
    
    # --- Rows and Columns ---
    rows_label = custom.Label(window_player_form, "Numero de filas:")
    rows_entry = custom.Entry(window_player_form)
    rows_entry.config(width=5)
    rows_notice = custom.Label(window_player_form, "Min:10", 10)

    center_widget(rows_label, window_width, window_height, y=260, w_divider=4, x_fraction=1)
    center_widget(rows_entry, window_width, window_height, y=290, w_divider=4, x_fraction=1)
    center_widget(rows_notice, window_width, window_height, y=320, w_divider=4, x_fraction=1)

    columns_label = custom.Label(window_player_form, "Numero de columnas:")
    columns_entry = custom.Entry(window_player_form)
    columns_entry.config(width=5)
    columns_notice = custom.Label(window_player_form, "Min:20", 10)

    center_widget(columns_label, window_width, window_height, y=260, w_divider=4, x_fraction=3)
    center_widget(columns_entry, window_width, window_height, y=290, w_divider=4, x_fraction=3)
    center_widget(columns_notice, window_width, window_height, y=320, w_divider=4, x_fraction=3)
    
    accept_button = custom.Button(
        window_player_form, 
        "Continue", 
        lambda: set_game_config(
            window_player_form,
            screen_width,
            screen_height,
            player_name1, 
            player_name2, 
            rows_entry, 
            columns_entry
        )
    )
    center_widget(accept_button, window_width, window_height, y=320, w_divider=2)

    window_player_form.protocol("WM_DELETE_WINDOW", sys.exit)
    return window_player_form

def create_welcome_screen(start_new_game, start_old_game) -> tk.Tk:
    """
    Create the welcome screen for the Battleship game.

    Args:
        start_new_game: Function to start a new game.
        start_old_game: Function to load an old game.

    Returns:
        tk.Tk: The welcome screen window.
    """
    window_menu = tk.Tk()
    window_menu.title("Menu")
    window_menu.configure(bg="white")
    
    window_width = int(screen_width // 2)
    window_height = int(screen_height // 2)

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_menu.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_menu.resizable(0, 0)

    welcome = custom.Label(window_menu, "¡Bienvenidos a Battleship!", 20)
    center_widget(welcome, window_width, window_height, y=20)

    load_game_btn = custom.Button(window_menu, "Cargar Partida", lambda: create_load_game_screen(window_menu, start_old_game).mainloop())
    center_widget(load_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=1)

    create_game_btn = custom.Button(window_menu, "Nueva Partida", lambda: start_new_game(window_menu))
    center_widget(create_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=3)

    window_menu.protocol("WM_DELETE_WINDOW", sys.exit)
    return window_menu
