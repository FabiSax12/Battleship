import tkinter                  as tk
import tk_logic.custom_widgets  as custom
from tkinter                    import messagebox
from tkinter                    import scrolledtext
from PIL                        import ImageTk, Image
from enum                       import Enum
from enums                      import Color, GameStage, Orientation, Ship
from game_data                  import game_data, load_game_data
from tk_logic.window_generators import screen_width, screen_height, create_player_info_frame, create_game_screen, create_new_game_screen, create_welcome_screen, update_player_info_frame
from game_logic.ships           import move_ships, print_all_ships, ships, ships_limit, generate_all_ship_images, place_ship_on_board, print_ship_image
from game_logic.board           import clean_board, generate_board, place_buttons_on_board, toggle_board, change_board_buttons_command

# Style
padding_x = None
padding_y = 50

def create_radio_buttons(window: tk.Tk, ships_complete_img: list, options: Enum, selected_variable: tk.StringVar, value_function):
    """
    Create radio buttons for the given options.

    Args:
        window (tk.Tk): The Tkinter window where the radio buttons will be placed.
        ships_complete_img (list): A list to store complete images of ships.
        options (Enum): An enumeration containing the options for the radio buttons.
        selected_variable (tk.StringVar): The Tkinter variable to store the selected option.
        value_function (function): A function that takes an option and returns its value.
        x (int): The x-coordinate where the radio buttons will be placed.
        y (int): The y-coordinate where the first radio button will be placed.

    Returns:
        tk.Label: The label containing the radio buttons.
    """
    container = tk.Frame(window)
    container.pack()

    for i, option in enumerate(options):
        image = Image.open(f"images/{option.value}.png")
        [image_width, image_height] = image.size
        image = image.resize((image_width // 5, image_height // 5))
        photo_image = ImageTk.PhotoImage(image)
        ships_complete_img.append(photo_image)

        radio_button = tk.Radiobutton(
            container,
            image=ships_complete_img[-1],
            text=option.value.capitalize(),
            variable=selected_variable,
            value=value_function(option),
            font=("Times New Roman", 12),
            foreground="black",
        )
        radio_button.pack(side=tk.TOP, anchor=tk.W)

def update_console(console: tk.Widget, message: str):
    console.config(state=tk.NORMAL)
    console.insert(tk.END, message + "\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)

def check_ship_hit(board: list, player_idx: int, oponent_idx: int, x: int, y: int, update_console: callable):
    ship_hit = False
    ships_list = game_data["board_1_ships"] if board == game_data["board_1"] else game_data["board_2_ships"]
    player = game_data["players"][player_idx]

    for ship_data in ships_list:
        ship_x = ship_data[0]
        ship_y = ship_data[1]
        ship = Ship[ship_data[2]]
        orientation = Orientation[ship_data[3]]
        ship_lenght = len(ships[ship])

        for i in range(ship_lenght):
            moved_x = ship_x
            moved_y = ship_y

            if orientation == Orientation.TOP:      moved_y += i
            elif orientation == Orientation.BOTTOM: moved_y -= i
            elif orientation == Orientation.LEFT:   moved_x += i
            elif orientation == Orientation.RIGHT:  moved_x -= i

            # If the shot hits a ship
            if moved_x == x and moved_y == y:
                ship_hit = True
                ship_data[4][i] = True
                board[y][x].config(background=Color.RED.value)

                x = x if board == game_data["board_1"] else x + game_data["board_columns"] // 2
                game_data["buttons_hit"].append([x, y])

                update_console(f"¡{player["nickname"]}, que puntería!")

                if ship_data[4].count(False) == 0:
                    game_data["players"][oponent_idx]["ships"][ship.value] -= 1
                    game_data["players"][player_idx]["points"] += len(ships[ship])

                    # Update the horizontal panel of the info
                    clean_board(game_data["board_1"])
                    clean_board(game_data["board_2"])
                    update_console(f"¡{player["nickname"]} ha hundido un {ship.name}!")
                    print_ship_image(ship, orientation, board, ship_x, ship_y)

    return ship_hit

def check_winner(oponent: dict):
    points_to_win = sum([ships_limit[ship] * len(ships[ship]) for ship in Ship])
    return oponent["points"] == points_to_win

def check_end_game(board: list, update_console):
    if game_data["game_stage"] == GameStage.END:
        for row in board:
            for btn in row:
                btn.config(state="disabled")
    else:
        toggle_board()

        if game_data["turn"] == 1:
            game_data["turn"] = 2
            player_nickname = game_data["players"][1]["nickname"]
            update_console(f"¡{player_nickname}, es tu turno!")
        else:
            move_ships(game_data["board_1_ships"])
            move_ships(game_data["board_2_ships"])

            game_data["turn"] = 1
            player_nickname = game_data["players"][0]["nickname"]
            update_console(f"¡{player_nickname}, es tu turno!")

def game_loop(x: int, y: int, board: list, update_frame: callable, frames_to_update: tuple[tk.Widget], update_console: callable):
    player_idx = game_data["turn"] - 1
    oponent_idx = 0 if player_idx == 1 else 1
    player = game_data["players"][player_idx]
    oponent = game_data["players"][oponent_idx]

    ship_hit = check_ship_hit(board, player_idx, oponent_idx, x, y, update_console)

    if not ship_hit:
        if check_winner(oponent):
            update_console("Fallaste tu última oportunidad")
            update_console(f"¡{oponent["nickname"]} hundido toda la flota enemiga!")
            update_console("Fin de la partida")
            game_data["game_stage"] = GameStage.END
        else:
            update_console("¡Vaya! No has dado en el blanco")
    else:
        if check_winner(player) and check_winner(oponent):
            update_console("¡Es un empate! Fin de la partida")
            game_data["game_stage"] = GameStage.END

    check_end_game(board, update_console)
    update_player_info_frame(frames_to_update[0], 0)
    update_player_info_frame(frames_to_update[2], 1)

def change_player_setup_turn(parent: tk.Widget, space_1: tk.Widget, space_3: tk.Widget):
    """
    Changes the player setup turn and updates the widget's position accordingly.

    Args:
        parent (tk.Widget): The Tkinter parent whose position will be updated.

    Returns:
        None
    """
    turn = game_data["turn"]
    board = game_data["board_1"] if turn == 1 else game_data["board_2"]
    player_ships = game_data["players"][turn - 1]["ships"]

    if (player_ships[Ship.DESTRUCTOR.value] < ships_limit[Ship.DESTRUCTOR] 
        or player_ships[Ship.CRUCERO.value] < ships_limit[Ship.CRUCERO]
        or player_ships[Ship.ACORAZADO.value] < ships_limit[Ship.ACORAZADO]
    ):
        messagebox.showinfo("Acción Inválida", "Aún no has colocado todos tus barcos")
    else:
        if turn == 1:
            clean_board(board)
            toggle_board()
            game_data["turn"] = 2
        else:
            clean_board(board)
            parent.pack_forget()
            
            for widget in parent.winfo_children():
                widget.destroy()

            game_data["game_stage"] = GameStage.PLAYING
            game_data["turn"] = 1
            
            player_nickname = game_data["players"][0]["nickname"]

            console = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Times New Roman", 14))
            console.pack()
            change_board_buttons_command(lambda board, x, y: game_loop(x, y, board, create_player_info_frame, (space_1, parent, space_3), lambda msj: update_console(console, msj)))

            update_player_info_frame(space_1, 0)
            update_player_info_frame(space_3, 1)
            update_console(console, "¡Que comience la batalla!")
            update_console(console, f"Turno de {player_nickname}")

def create_horizontal_spaces(window):
    # Obtener el ancho y la altura de la ventana
    window_width = screen_width
    window_height = screen_height

    # Calcular el ancho de cada espacio horizontal
    space_width = window_width / 3 - window_width * (0.2 / 3)
    space_height = window_height / 3

    container = tk.Frame(window)
    container.pack_propagate(False)
    container.place(x=window_width * 0.1, y=padding_y + game_data["button_width"] * game_data["board_rows"] + 50)

    # Crear tres frames para representar los espacios horizontales
    space1 = tk.Frame(container, width=space_width, height=space_height)
    space2 = tk.Frame(container, width=space_width, height=space_height)
    space3 = tk.Frame(container, width=space_width, height=space_height)
    space1.pack_propagate(False)
    space2.pack_propagate(False)
    space3.pack_propagate(False)

    # Configurar el tamaño de los espacios horizontales
    space1.grid(row=0, column=0)
    space2.grid(row=0, column=1)
    space3.grid(row=0, column=2)

    return space1, space2, space3

def setup_game_screen(game_screen: tk.Tk, ships_complete_img: list, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Sets up the game screen with necessary labels and widgets.

    Args:
        game_screen (tk.Tk): The Tkinter window object representing the game screen.
        ships_complete_img (list): A list of complete ship images.
        selected_ship (tk.StringVar): A Tkinter variable storing the selected ship.
        selected_orientation (tk.StringVar): A Tkinter variable storing the selected orientation.

    Returns:
        None
    """
    setup_div = tk.Frame(game_screen)

    setup_div_label = custom.Label(setup_div, "Selecciona un barco y su orientación")
    setup_div_label.pack()

    ships_orientation_container = tk.Frame(setup_div)
    ships_selector_div = tk.Frame(ships_orientation_container)
    orientation_selector_div = tk.Frame(ships_orientation_container)

    ships_selector_div.pack(side=tk.LEFT, padx=5)
    orientation_selector_div.pack(side=tk.LEFT, padx=5)
    ships_orientation_container.pack()

    create_radio_buttons(ships_selector_div, ships_complete_img, ships, selected_ship, lambda ship: ship.name)
    create_radio_buttons(orientation_selector_div, ships_complete_img, Orientation, selected_orientation, lambda orientation: orientation.name)

    ships_placed_container = tk.Frame(setup_div)
    ships_placed_container.pack()

    ships_placed_button = custom.Button(ships_placed_container, "Guardar posiciones")
    ships_placed_button.pack(side=tk.TOP, pady=30)

    return setup_div, ships_placed_button

def init_game(game_mode: str):
    global padding_x

    board_columns = game_data["board_columns"]
    button_width = game_data["button_width"]
    padding_x = (screen_width // 2) - (button_width * (board_columns // 2 + 0.5))

    game_screen = create_game_screen()
    generate_board(game_screen, padding_x)

    space_1, space_2, space_3 = create_horizontal_spaces(game_screen)
    create_player_info_frame(space_1, 0).pack()
    create_player_info_frame(space_3, 1).pack()

    generate_all_ship_images()

    if game_mode == "old":
        place_buttons_on_board(game_data["board_1"], padding_x)
        place_buttons_on_board(game_data["board_2"], padding_x + (game_data["button_width"] * (board_columns // 2 + 1)))

    return game_screen, space_1, space_2, space_3

def start_new_game(window: tk.Tk):
    """
    Initialize a new game with a new game screen.

    Args:
        window (tk.Tk): The Tkinter window object.

    Returns:
        None
    """

    window.destroy()
    window_new_game = create_new_game_screen()
    window_new_game.mainloop()
    
    game_screen, space_1, space_2, space_3 = init_game("new")
    
    selected_ship = tk.StringVar(value=Ship.DESTRUCTOR.name)
    selected_orientation = tk.StringVar(value=Orientation.TOP.name)
    ships_complete_img = []
    change_board_buttons_command(
        lambda board, x, y: place_ship_on_board(board, x, y, selected_ship, selected_orientation, update_player_info_frame, (space_1, space_3))
    )

    setup_div, button = setup_game_screen(space_2, ships_complete_img, selected_ship, selected_orientation)
    setup_div.pack()
    button.bind("<Button-1>", lambda event: change_player_setup_turn(space_2, space_1, space_3))

    game_screen.mainloop()

def start_old_game(file_name: str):
    """
    Load a saved game and initialize the game interface.

    Args:
        file_name (str): The name of the file containing the saved game.

    Returns:
        None
    """
    load_game_data(file_name)

    game_screen, space_1, space_2, space_3 = init_game("old")

    if game_data["game_stage"] == GameStage.PLACING_SHIPS:
        selected_ship = tk.StringVar(value=Ship.DESTRUCTOR.name)
        selected_orientation = tk.StringVar(value=Orientation.TOP.name)
        ships_complete_img = []
        setup_div, button = setup_game_screen(space_2, ships_complete_img, selected_ship, selected_orientation)
        setup_div.pack()
        button.bind("<Button-1>", lambda event: change_player_setup_turn(space_2, space_1, space_3))

        if game_data["turn"] == 1:
            for ship in game_data["board_1_ships"]:
                print_ship_image(Ship[ship[2]], Orientation[ship[3]], game_data["board_1"], ship[0], ship[1])

        elif game_data["turn"] == 2:
            for ship in game_data["board_2_ships"]:
                print_ship_image(Ship[ship[2]], Orientation[ship[3]], game_data["board_2"], ship[0], ship[1])

        change_board_buttons_command(lambda board, x, y: place_ship_on_board(board, x, y, selected_ship, selected_orientation, update_player_info_frame, (space_1, space_3)))
    elif game_data["game_stage"] == GameStage.PLAYING:
        print_all_ships(game_data["board_1_ships"], game_data["board_1"])
        print_all_ships(game_data["board_2_ships"], game_data["board_2"])
        clean_board(game_data["board_1"])
        clean_board(game_data["board_2"])
        toggle_board()
        console = scrolledtext.ScrolledText(space_2, wrap=tk.WORD, font=("Times New Roman", 14))
        console.pack()
        change_board_buttons_command(lambda board, x, y: game_loop(x, y, board, create_player_info_frame, (space_1, space_2, space_3), lambda msj: update_console(console, msj)))
        update_console(console, "¡La batalla debe continuar!")
        update_console(console, f"Turno de {game_data["players"][game_data["turn"] - 1]["nickname"]}")

    game_screen.mainloop()

def main():
    window_menu = create_welcome_screen(start_new_game, start_old_game)
    window_menu.mainloop()

if __name__ == "__main__":
    main()