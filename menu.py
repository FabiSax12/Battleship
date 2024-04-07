#To create window.
#Remember that everything you want change in the window must be placed inside the mainloop.
import tkinter
def player_registration():
    window_player_registration = tkinter.Tk()
    window_player_registration.title("Menú")
    window_player_registration.geometry("500x500")
    window_player_registration.resizable(0,0)
    game_log = tkinter.Label(window_player_registration, text = "Registro de Jugadores", font = ("Times New Roman", 20))
    game_log.place(x = 125, y = 40)
    
    player1 = tkinter.Label(window_player_registration, text = "Coloque el nombre del jugador 1:", font = ("Times New Roman", 15))
    player1.place(x = 10, y = 125)
    player_name1 = tkinter.Entry(window_player_registration, font = ("Times New Roman", 15))
    player_name1.place(x = 10, y = 160)
    
    player2 = tkinter.Label(window_player_registration, text = "Coloque el nombre del jugador 2:", font = ("Times New Roman", 15) )
    player2.place(x = 10, y = 190)
    player_name2 = tkinter.Entry(window_player_registration, font = ("Times New Roman", 15))
    player_name2.place(x = 10, y = 220)
    
    accept_button = tkinter.Button(window_player_registration, text = "Continuar", font = ("Times New Roman", 17), bg = "black", fg = "white" )
    accept_button.place(x = 200, y = 260)
    
    window_player_registration.mainloop()

window_menu = tkinter.Tk() #to initialize a window object.
window_menu.title("Menú") #To insert the tittle.
window_menu.configure(bg = "white")
window_menu.geometry("500x500") #To size the window.
window_menu.resizable(0,0) #Whit this the window size can´t change.


#To create labels.
#In the parentheses we place the window to wich the label is linked and after comma the type of label.
#"font" is to change the font and letter size.
welcome = tkinter.Label(window_menu, text = "¡Bienvenidos jugadores!", font = ("Times New Roman", 20)).place(x = 123, y = 135) #".pack()" , "place()" or "grid()" it´s necessary for the label to be displayed in the window.
registration = tkinter.Label(window_menu, text = "¿Desean registrarse?", font = ("Times New Roman", 17)).place(x = 160, y = 185)

#To create button.
#def salir():
yes_button = tkinter.Button(window_menu, text = "Sí", font = ("Times New Roman", 15), bg = "black", fg = "white", command = player_registration).place(x = 123, y = 260, height = 50, width = 100) 
no_button = tkinter.Button(window_menu, text = "No", font = ("Times New Roman", 15), bg = "black", fg = "white").place(x = 285, y = 260, height = 50, width = 100) 

    

window_menu.mainloop() #This keeps the window open inside cmd.