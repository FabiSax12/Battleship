import tkinter          as tk
import tk_logic.custom_widgets as custom
from tkinter            import messagebox
from game_data          import game_data, save_game_data

players = game_data["players"]

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

def register_players(name: str):
    new_player = {
        "nickname": name,
        "poins": 0,
        "ships": {
            "acorazado": 0,
            "crucero": 0,
            "destructor": 0
        }
    }

    players.append(new_player)

def set_game_config(window, player_name1: tk.Entry, player_name2: tk.Entry, rows_box: tk.Entry, columns_box: tk.Entry):
    name1 = player_name1.get()
    name2 = player_name2.get()
    
    if name1 == "" or name2 == "":
        tk.messagebox.showinfo("Error", "Debe registrar los jugadores.")
        return
        
    elif name1 == name2:
        tk.messagebox.showinfo("Error", "Los nombres de los jugadores deben ser diferentes.")
        return
        
   
    try:
        rows = int(rows_box.get())
        
        if  rows < 10:
            tk.messagebox.showinfo("Error", "El número de filas debe ser mínimo 10.")
            return
            
        else:
            game_data["board_rows"] = rows
            
    except ValueError:
        tk.messagebox.showinfo("Error", "El número de filas debe ser un número entero positivo.")
        return
        
    try:
        columns = int(columns_box.get())

        game_data["button_width"] = (screen_width - 300) // (columns + 1)
        
        if  columns < 20:
            tk.messagebox.showinfo("Error", "El número de columnas debe ser mínimo 20.")
            return
            
        elif columns % 2 != 0:
            tk.messagebox.showinfo("Error", "El número de columnas debe ser PAR.")
            return
            
        else:
            game_data["board_columns"] = columns

    except ValueError:
        tk.messagebox.showinfo("Error", "El número de columnas debe ser un número entero positivo.")
        return
          
    register_players(name1)
    register_players(name2)
    
    window.destroy()

def center_window(window: tk.Tk, window_width: int, window_height: int) -> list:
    pos_x = screen_width // 2 - window_width // 2
    pos_y = screen_height // 2 - window_height // 2

    return [pos_x, pos_y]

def center_widget(widget: tk.Widget, window_width: int, window_height: int, x = None, y = None, w_divider = 2, h_divider = 2, x_fraction = 1, y_fraction = 1) -> list:
    widget_width = widget.winfo_reqwidth()
    widget_height = widget.winfo_reqheight()

    new_x = x if x else window_width // w_divider * x_fraction - widget_width // 2
    new_y = y if y else window_height // h_divider * y_fraction - widget_height // 2

    widget.place_configure(x=new_x, y=new_y)

def create_save_game_screen() -> tk.Tk:
    window_save_game = tk.Tk()
    window_save_game.title("Guardar Partida")
    
    window_width = screen_width // 4
    window_height = screen_height // 2

    [pos_x, pos_y] = center_window(window_save_game, window_width, window_height)

    window_save_game.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_save_game.resizable(0, 0)

    save_game_label = custom.Label(window_save_game, "Nombre de la partida:")
    center_widget(save_game_label, window_width, window_height, y=window_height // 10)

    save_game_entry = custom.Entry(window_save_game)
    center_widget(save_game_entry, window_width, window_height, y=window_height // 10 + 50)

    save_game_button = custom.Button(window_save_game, "Guardar", lambda: save_game_data(save_game_entry.get()))
    center_widget(save_game_button, window_width, window_height, y=window_height // 10 + 100)

    other_saved_games = tk.Frame(window_save_game, height=window_height // 2)
    other_saved_games.place(x=0, y=window_height // 2, width=window_width)
    
    scrollbar = tk.Scrollbar(other_saved_games, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(other_saved_games, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=50)
    
    custom.Label(other_saved_games, "Sobrescribir partida guardada").place(x=0, y=0)

    for file_name in game_data["saved_games"]:
        listbox.insert(tk.END, file_name)

    listbox.bind("<Double-Button-1>", lambda event: save_game_data(listbox.get(listbox.curselection()[0])))

    scrollbar.config(command=listbox.yview)

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

    [pos_x, pos_y] = center_window(window_player_form, window_width, window_height)

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

    [pos_x, pos_y] = center_window(window_menu, window_width, window_height)

    window_menu.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window_menu.resizable(0, 0)

    welcome = custom.Label(window_menu,"¡Bienvenidos a Battleship!", 20)
    center_widget(welcome, window_width, window_height, y=20)

    load_game_btn = custom.Button(window_menu, "Cargar Partida", lambda: start_old_game(window_menu))
    center_widget(load_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=1)

    create_game_btn = custom.Button(window_menu, "Crear partida", lambda: start_new_game(window_menu))
    center_widget(create_game_btn, window_width, window_height, y=260, w_divider=4, x_fraction=3)

    window_menu.protocol("WM_DELETE_WINDOW", exit)
    return window_menu
