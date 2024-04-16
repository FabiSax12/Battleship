from calendar import c
import tkinter          as tk
import tk_logic.custom_widgets as custom
from tkinter            import messagebox
from game_data          import find_saved_games, game_data, save_game_data
from game_logic.config  import set_game_config

players = game_data["players"]

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

def center_window(window_width: int, window_height: int) -> list:
    pos_x = screen_width // 2 - window_width // 2
    pos_y = screen_height // 2 - window_height // 2

    return [pos_x, pos_y]

def center_widget(widget: tk.Widget, window_width: int, window_height: int, x = None, y = None, w_divider = 2, h_divider = 2, x_fraction = 1, y_fraction = 1) -> list:
    widget_width = widget.winfo_reqwidth()
    widget_height = widget.winfo_reqheight()

    new_x = x if x else window_width // w_divider * x_fraction - widget_width // 2
    new_y = y if y else window_height // h_divider * y_fraction - widget_height // 2

    widget.place_configure(x=new_x, y=new_y)

def list_of_saved_games(parent_window, title, action) -> tk.Frame:
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
    window.destroy()

    window_load_game = tk.Tk()
    window_load_game.title("Cargar Partida")

    window_width = screen_width // 4
    window_height = screen_height // 2

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_load_game.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_load_game.resizable(0, 0)

    saved_games_list = list_of_saved_games(window_load_game, "Partidas Guardadas", start_old_game)
    saved_games_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=50, pady=50)
    
    return window_load_game

def create_save_game_screen() -> tk.Tk:
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
    saved_games_list.config(height=window_height // 2, width=window_width)
    saved_games_list.place(x=0, y=window_height // 2)

    return window_save_game

def create_game_screen() -> tk.Tk:
    # Graphic Interface
    game_screen = tk.Tk()
    game_screen.title("Battleship")
    game_screen.protocol("WM_DELETE_WINDOW", exit)
    game_screen.state("zoomed")
    custom.Button(game_screen, "Guardar", lambda: create_save_game_screen().mainloop()).place(x=0, y=0)
    return game_screen

def create_new_game_screen() -> tk.Tk:
    window_player_form = tk.Tk()

    window_player_form.title("Menú")
    
    window_width = int(screen_width // 2)
    window_height = int(screen_height // 2)

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_player_form.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_player_form.resizable(0,0)
    
    game_log = custom.Label(window_player_form, "Registro de Jugadores", 17)
    center_widget(game_log, window_width, window_height, y=20)
    
    player1 = custom.Label(window_player_form, "Nombre del jugador 1:")
    center_widget(player1, window_width, window_height, y=100, w_divider=4, x_fraction=1)
    player_name1 = custom.Entry(window_player_form)
    center_widget(player_name1, window_width, window_height, y=150, w_divider=4, x_fraction=1)

    player2 = custom.Label(window_player_form, "Nombre del jugador 2:")
    center_widget(player2, window_width, window_height, y=100, w_divider=4, x_fraction=3)
    player_name2 = custom.Entry(window_player_form)
    center_widget(player_name2, window_width, window_height, y=150, w_divider=4, x_fraction=3)
    
    game_settings = custom.Label(window_player_form, "Configuración del Tablero", 17)
    center_widget(game_settings, window_width, window_height, y=200)
    
    # --- Rows and Columns ---
    rows_label = custom.Label(window_player_form, "Número de filas:")
    rows_entry = custom.Entry(window_player_form)
    rows_entry.config(width=5)
    rows_notice = custom.Label(window_player_form, "Min:10", 10)

    center_widget(rows_label, window_width, window_height, y=260, w_divider=4, x_fraction=1)
    center_widget(rows_entry, window_width, window_height, y=290, w_divider=4, x_fraction=1)
    center_widget(rows_notice, window_width, window_height, y=320, w_divider=4, x_fraction=1)


    columns_label = custom.Label(window_player_form, "Número de columnas:")
    columns_entry = custom.Entry(window_player_form)
    columns_entry.config(width=5)
    columns_notice = custom.Label(window_player_form, "Min:20", 10)

    center_widget(columns_label, window_width, window_height, y=260, w_divider=4, x_fraction=3)
    center_widget(columns_entry, window_width, window_height, y=290, w_divider=4, x_fraction=3)
    center_widget(columns_notice, window_width, window_height, y=320, w_divider=4, x_fraction=3)
    
    
    accept_button = custom.Button(
        window_player_form, 
        "Continuar", 
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

    window_player_form.protocol("WM_DELETE_WINDOW", exit)
    return window_player_form

def create_welcome_screen(start_new_game, start_old_game) -> tk.Tk:

    window_menu = tk.Tk()
    window_menu.title("Menú")
    window_menu.configure(bg = "white")
    
    window_width = int(screen_width // 2)
    window_height = int(screen_height // 2)

    [pos_x, pos_y] = center_window(window_width, window_height)

    window_menu.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_menu.resizable(0, 0)

    welcome = custom.Label(window_menu,"¡Bienvenidos a Battleship!", 20)
    center_widget(welcome, window_width, window_height, y=20)

    load_game_btn = custom.Button(window_menu, "Cargar Partida", lambda: create_load_game_screen(window_menu, start_old_game).mainloop())
    center_widget(load_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=1)

    create_game_btn = custom.Button(window_menu, "Crear partida", lambda: start_new_game(window_menu))
    center_widget(create_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=3)

    window_menu.protocol("WM_DELETE_WINDOW", exit)
    return window_menu