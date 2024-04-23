import tkinter as tk
from game_data import game_data

players = game_data["players"]

def register_players(name: str):
    """
    Register a new player with the given name.

    Args:
        name: The name of the player.
    """
    new_player = {
        "nickname": name,
        "points": 0,
        "ships": {
            "acorazado": 0,
            "crucero": 0,
            "destructor": 0
        }
    }

    players.append(new_player)

def set_game_config(window, screen_width, screen_height, player_name1: tk.Entry, player_name2: tk.Entry, rows_box: tk.Entry, columns_box: tk.Entry):
    """
    Set the game configuration based on user input.

    Args:
        window: The Tkinter window.
        screen_width: The width of the screen.
        screen_height: The height of the screen.
        player_name1: The Tkinter Entry widget containing the name of player 1.
        player_name2: The Tkinter Entry widget containing the name of player 2.
        rows_box: The Tkinter Entry widget containing the number of rows.
        columns_box: The Tkinter Entry widget containing the number of columns.
    """
    name1 = player_name1.get()
    name2 = player_name2.get()
    
    if name1 == "" or name2 == "":
        tk.messagebox.showinfo("Error", "Debe registrar los jugadores.")
        return
        
    elif name1 == name2:
        tk.messagebox.showinfo("Error", "Los nombres de los jugadores deben ser diferentes.")
        return
        
    button_width = 0
    button_height = 0
    max_rows = screen_height // 2 // 19
    max_cols = (screen_width - 300) // 19

    try:
        rows = int(rows_box.get())

        button_height = screen_height // 2 // rows

        if button_height < 19:
            tk.messagebox.showinfo("Error", f"{rows} filas es excesivo, el máximo para la resolución de tu pantalla es {max_rows}.")
            return
        
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

        button_width = (screen_width - 300) // (columns + 1)
        
        print(button_width, max_cols)
        if button_width < 19:
            tk.messagebox.showinfo("Error", f"{columns} columnas es excesivo, el máximo para la resolución de tu pantalla es {max_cols - 1}.")
            return

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
          
    game_data["button_width"] = button_width if button_width < button_height else button_height

    register_players(name1)
    register_players(name2)
    
    window.destroy()
