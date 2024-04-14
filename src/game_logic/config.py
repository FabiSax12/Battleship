import tkinter as tk
from game_data import game_data

players = game_data["players"]

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

def set_game_config(window, screen_width, player_name1: tk.Entry, player_name2: tk.Entry, rows_box: tk.Entry, columns_box: tk.Entry):
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