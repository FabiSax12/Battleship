import tkinter as tk

players = []

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
    print(players)

def register_players_and_close_window(window, player_name1: tk.Entry, player_name2: tk.Entry):
    name1 = player_name1.get()
    name2 = player_name2.get()
    register_players(name1)
    register_players(name2)
    window.destroy()

def player_registration():
    window_menu.destroy()
    
    window_player_form = tk.Tk()

    window_player_form.title("Menú")
    window_player_form.geometry("500x500")
    window_player_form.resizable(0,0)

    game_log = tk.Label(window_player_form, text="Registro de Jugadores", font=("Times New Roman", 20))
    game_log.place(x=125, y=40)

    player1 = tk.Label(window_player_form, text="Coloque el nombre del jugador 1:", font=("Times New Roman", 15))
    player1.place(x=10, y=125)
    player_name1 = tk.Entry(window_player_form, font=("Times New Roman", 15))
    player_name1.place(x=10, y=160)

    player2 = tk.Label(window_player_form, text="Coloque el nombre del jugador 2:", font=("Times New Roman", 15))
    player2.place(x=10, y=190)
    player_name2 = tk.Entry(window_player_form, font=("Times New Roman", 15))
    player_name2.place(x=10, y=220)

    accept_button = tk.Button(window_player_form, 
                              text="Continuar", 
                              font=("Times New Roman", 17), 
                              bg="black", 
                              fg="white",
                              command=lambda: register_players_and_close_window(window_player_form, player_name1, player_name2)
                            )
    accept_button.place(x=200, y=260)

    window_player_form.mainloop()

window_menu.title("Menú") #insert the tittle.
window_menu.configure(bg = "white")
window_menu.geometry("550x500") #size the window.
window_menu.resizable(0, 0) #Whit this the window size can´t change.


#create labels.
#In the parentheses we place the window to wich the label is linked and after comma the type of label.
#"font" is to change the font and letter size.
welcome = tk.Label(window_menu, text = "¡Bienvenidos a Battleship!", font = ("Times New Roman", 20)).place(x = 123, y = 135)
# registration = tk.Label(window_menu, text = "¿Desean registrarse?", font = ("Times New Roman", 17)).place(x = 160, y = 185)

#create button.
load_game_btn = tk.Button(window_menu, text = "Cargar Partida", font = ("Times New Roman", 15), bg = "black", fg = "white").place(x = 123, y = 260, height = 50, width = 150) 
create_game_btn = tk.Button(window_menu, text = "Crear partida", font = ("Times New Roman", 15), bg = "black", fg = "white", command = player_registration).place(x = 285, y = 260, height = 50, width = 150) 

window_menu.mainloop() #This keeps the window open inside cmd.