import tkinter as tk
from game_data import players, board_colums, board_rows
from tkinter import messagebox
import tk_widgets.custom_tk_widgets as custom

window_menu = tk.Tk()

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
    global board_colums
    global board_rows
    
    name1 = player_name1.get()
    name2 = player_name2.get()
    
    if name1 == "" or name2 == "":
        tk.messagebox.showinfo("Error", "Debe registrar los jugadores.")
        window.mainloop()
    elif name1 == name2:
        tk.messagebox.showinfo("Error", "Los nombres de los jugadores deben ser diferentes.")
        window.mainloop()
   
    try:
        rows = int(rows_box.get())
        
        if  rows < 10:
            tk.messagebox.showinfo("Error", "El número de filas debe ser mínimo 10.")
            window.mainloop()

        else:
            global board_rows 
            board_rows = rows
            
    except ValueError:
        tk.messagebox.showinfo("Error", "El número de filas debe ser un número entero positivo.")
        window.mainloop()
    try:
        columns = int(columns_box.get())
        
        if  columns < 20:
            tk.messagebox.showinfo("Error", "El número de columnas debe ser mínimo 20.")
            window.mainloop()
        elif columns % 2 != 0:
            tk.messagebox.showinfo("Error", "El número de columnas debe ser PAR.")
            window.mainloop()
        else:
            global board_colums 
            board_colums = columns
    except ValueError:
         tk.messagebox.showinfo("Error", "El número de columnas debe ser un número entero positivo.")
         window.mainloop() 

    register_players(name1)
    register_players(name2)
    
    window.destroy()

def player_registration():
    window_menu.destroy()
    
    window_player_form = tk.Tk()

    window_player_form.title("Menú")
    window_player_form.geometry("580x450")
    window_player_form.resizable(0,0)
    
    game_log = custom.Label(window_player_form, "Registro de Jugadores", 17)
    game_log.place(x=187, y=20)
    
    player1 = custom.Label(window_player_form, "Nombre del jugador 1:")
    player1.place(x=43, y=85)
    player_name1 = custom.Entry(window_player_form)
    player_name1.place(x=40, y=131)

    player2 = custom.Label(window_player_form, "Nombre del jugador 2:")
    player2.place(x=340, y=85)
    player_name2 = custom.Entry(window_player_form)
    player_name2.place(x=340, y=131)
    
    game_settings = custom.Label(window_player_form, "Configuración del Juego", 17)
    game_settings.place(x=178, y=205)
    
    
    rows = custom.Label(window_player_form, "Número de filas:")
    rows.place(x = 43, y = 260)
    rows_notice = custom.Label(window_player_form, "Min:10", 10)
    rows_notice.place(x = 180, y = 287)
    rows_box = custom.Entry(window_player_form)
    rows_box.place(x=180, y=260, width= 50)
    
    columns = custom.Label(window_player_form, "Número de columnas:")
    columns.place(x = 305, y = 260)
    columns_notice = custom.Label(window_player_form, "Min:20", 10)
    columns_notice.place(x = 485, y = 287)
    columns_entry = custom.Entry(window_player_form)
    columns_entry.place(x=485, y=260, width= 50)
    

    accept_button = custom.Button(window_player_form, "Continuar", lambda: set_game_config(window_player_form, player_name1, player_name2, rows_box, columns_entry))
    accept_button.place(x=235, y=355)

    window_player_form.mainloop()

window_menu.title("Menú") #insert the tittle.
window_menu.configure(bg = "white")
window_menu.geometry("550x500") #size the window.
window_menu.resizable(0, 0) #Whit this the window size can´t change.


#create labels.
#In the parentheses we place the window to wich the label is linked and after comma the type of label.
#"font" is to change the font and letter size.
welcome = custom.Label(window_menu,"¡Bienvenidos a Battleship!", 20)
# welcome = tk.Label(window_menu, text = "¡Bienvenidos a Battleship!")
welcome.place(x = 123, y = 135)
# registration = tk.Label(window_menu, text = "¿Desean registrarse?", font = ("Times New Roman", 17)).place(x = 160, y = 185)

#create button.
load_game_btn = custom.Button(window_menu, "Cargar Partida")
load_game_btn.place(x = 123, y = 260, height = 50, width = 150) 

create_game_btn = custom.Button(window_menu, "Crear partida", player_registration)
create_game_btn.place(x = 285, y = 260, height = 50, width = 150) 

window_menu.mainloop() #This keeps the window open inside cmd.