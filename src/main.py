import stat
import tkinter      as tk
from tkinter.font   import Font
from turtle import setup
from PIL            import ImageTk, Image
from enum           import Enum

import tk_widgets.custom_tk_widgets as custom
from game_data      import ships, ships_Tkinter_images, game_data
from enums          import Orientation, Ship
from GUI_game       import create_game_screen, create_new_game_screen, create_welcome_screen, screen_height, screen_width

board_1 = game_data["board_1"]
board_2 = game_data["board_2"]

# Style
padding_x = None
padding_y = 50

def print_ship_image(ship: Ship, orientation: Orientation, board: list, x: int, y: int):
    """
    Prints the image of a ship on the game board.

    Args:
        ship (Ship): The type of ship to print.
        orientation (Orientation): The orientation of the ship.
        board (list): The game board represented as a 2D list.
        x (int): The x-coordinate of the starting position for the ship.
        y (int): The y-coordinate of the starting position for the ship.
    """

    for i in range(len(ships[ship])):
        moved_x = x
        moved_y = y

        if orientation == Orientation.TOP:      moved_y += i
        elif orientation == Orientation.BOTTOM: moved_y -= i
        elif orientation == Orientation.LEFT:   moved_x += i
        elif orientation == Orientation.RIGHT:  moved_x -= i

        if 0 <= moved_x < len(board[0]) and 0 <= moved_y < len(board):
            button: tk.Button = board[moved_y][moved_x]
            button.config(image=ships_Tkinter_images[ship][orientation][i])

def validate_ship_position(x: int, y: int, ship: Ship, orientation: Orientation, board: list):
    """
    Validates the position of a ship on the game board.

    Args:
        x (int): The x-coordinate of the starting position for the ship.
        y (int): The y-coordinate of the starting position for the ship.
        ship (Ship): The type of ship to validate.
        orientation (Orientation): The orientation of the ship.
        board (list): The game board represented as a 2D list.

    Returns:
        bool: True if the ship can be placed on the board, False otherwise.
    """
    for i in range(len(ships[ship])):
        moved_x = x
        moved_y = y

        if orientation == Orientation.TOP:      moved_y += i
        elif orientation == Orientation.BOTTOM: moved_y -= i
        elif orientation == Orientation.LEFT:   moved_x += i
        elif orientation == Orientation.RIGHT:  moved_x -= i

        if 0 <= moved_x < len(board[0]) and 0 <= moved_y < len(board):
            button: tk.Button = board[moved_y][moved_x]
            if button["image"] != "":
                return False
        else:
            return False

    return True

def posisionate_ship(x: int, y: int, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Handles the click event on the game board.

    Args:
        x (int): The x-coordinate of the clicked position on the game board.
        y (int): The y-coordinate of the clicked position on the game board.
    """
    board_columns = game_data["board_columns"]

    board_clicked = board_1 if x < board_columns // 2 else board_2

    x = x - board_columns // 2 if x >= board_columns // 2 else x

    if validate_ship_position(x, y, Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked):
        print_ship_image(Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked, x, y)
    
def colocate_buttons_on_screen(board: list, placement_x: int = None):
    """
    Positions the buttons on the game screen based on the provided board and placement coordinates.

    Args:
        board (list): The game board containing the buttons.
        placement_x (int): The x-coordinate where the buttons will be placed on the screen.
    """
    board_columns = game_data["board_columns"]
    button_width = game_data["button_width"]
    placement_x = padding_x if placement_x is None else placement_x

    x_offset = button_width if len(board[0]) > board_columns // 2 else 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            btn = board[row][col]
            x_pos = placement_x + col * button_width + (col // (board_columns // 2)) * x_offset
            y_pos = padding_y + row * button_width
            btn.place(x=x_pos, y=y_pos, width=button_width, height=button_width)

def generate_board(window: tk.Tk, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Generates the game boards, initializes buttons, and places them on the game screen.

    This function creates two game boards, initializes buttons for each cell, and then places these buttons on the game screen.
    """
    global board_1
    global board_2

    board_rows = game_data["board_rows"]
    board_columns = game_data["board_columns"]

    game_board = [
        [
            tk.Button(window, 
                      command=lambda x=col, y=row: posisionate_ship(x, y, selected_ship, selected_orientation),
                      state="disabled" if col < board_columns // 2 else "normal",
                      background="lightBlue", 
                      activebackground="lightBlue",
                      borderwidth=1,
                      relief="solid",
                      compound="center",
                      cursor="crosshair"
                    )

            for col in range(board_columns)
        ] 
        for row in range(board_rows)
    ]

    board_1 = [game_board[row][0 : board_columns // 2] for row in range(board_rows)]
    board_2 = [game_board[row][board_columns // 2:   ] for row in range(board_rows)]
    toggle_board()

    colocate_buttons_on_screen(board_1)
    colocate_buttons_on_screen(board_2, padding_x + (game_data["button_width"] * (board_columns // 2 + 1)))

def generate_all_ship_images():
    """
    Generates images of all ships in all orientations.

    This function iterates over all ships and orientations, loads their respective images, resizes them to match the button size,
    and rotates them based on the orientation. It then converts the rotated images into PhotoImage objects and stores them in the
    ships_Tkinter_images dictionary.
    """
    button_width = game_data["button_width"]

    for ship in ships.keys():
        for orientation in ships_Tkinter_images[ship].keys():
            for image_path in ships[ship]:
                image = Image.open(f"src/images/{image_path}")
                image = image.resize((button_width, button_width))
                
                if orientation == Orientation.LEFT:     rotated_image = image.rotate(180)
                elif orientation == Orientation.RIGHT:  rotated_image = image.rotate(0)
                elif orientation == Orientation.TOP:    rotated_image = image.rotate(90)
                elif orientation == Orientation.BOTTOM: rotated_image = image.rotate(270)
                
                if isinstance(rotated_image, Image.Image):
                    photo_image = ImageTk.PhotoImage(rotated_image)
                    ships_Tkinter_images[ship][orientation].append(photo_image)

def enable_board(board: list):
    for row in board:
        for btn in row:
            btn.config(state="normal")

def toggle_board():
    for row in board_1:
        for btn in row:
            state = btn["state"]
            btn.config(state="normal" if state == "disabled" else "disabled")

    for row in board_2:
        for btn in row:
            state = btn["state"]
            btn.config(state="normal" if state == "disabled" else "disabled")

def create_radio_buttons(window: tk.Tk, ships_complete_img: list, options: Enum, selected_variable: tk.StringVar, value_function, x: int, y: int):
    """
    Create radio buttons for the given options.

    Args:
        window: The Tkinter window where the radio buttons will be placed.
        options: A list of options for the radio buttons.
        selected_variable: The Tkinter variable to store the selected option.
        value_function: A function that takes an option and returns its value.
        x: The x-coordinate where the radio buttons will be placed.
        y: The y-coordinate where the first radio button will be placed.
    """
    radio_label = custom.Label(window, "Seleccione un barco", 12, height=300)
    radio_label.place(x=x, y=y)

    for i, option in enumerate(options):
        image = Image.open(f"src/images/{option.value}.png")
        [image_width, image_height] = image.size
        image = image.resize((image_width // 5, image_height // 5))
        photo_image = ImageTk.PhotoImage(image)
        ships_complete_img.append(photo_image)

        radio_button = tk.Radiobutton(
            radio_label,
            image=ships_complete_img[-1],
            text=option.value.capitalize(),
            variable=selected_variable,
            value=value_function(option),
            font=("Times New Roman", 12),
            foreground="black",
        )
        radio_button.place(x=radio_label.winfo_x() // 2 - radio_button.winfo_width(), y=radio_label.winfo_y() + 30 * i + 30)

    return radio_label

def move_widget(widget: tk.Widget, new_x, new_y):
    toggle_board()
    widget.place_forget()
    widget.place_configure(x=new_x, y=new_y)

def setup_game_screen(game_screen: tk.Tk, ships_complete_img: list, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Sets up the game screen with necessary labels and widgets.
    """
    board_columns = game_data["board_columns"]
    button_width = game_data["button_width"]

    game_state_label = tk.Label(game_screen, text="Posicione sus barcos", font=Font(family="Times New Roman", size=17))
    game_state_label.place(x=padding_x, y=padding_y - 50)

    setup_div = tk.Label(game_screen, text="Seleccione un barco y una orientación", font=("Times New Roman", 12), height=300)

    ships_selector_div = create_radio_buttons(setup_div, ships_complete_img, ships, selected_ship, lambda ship: ship.name, 0, 20)
    orientation_selector_div = create_radio_buttons(setup_div, ships_complete_img, Orientation, selected_orientation, lambda orientation: orientation.name, 200, 20)

    ships_placed_button = custom.Button(
        setup_div, 
        "Guardar Posiciones",
        lambda: move_widget(setup_div, padding_x + (button_width * ((board_columns // 2) + 1)), 500)
    )
    ships_placed_button.place(x=setup_div.winfo_reqwidth() // 2 - 50, y=250)

    setup_div.configure(width=ships_selector_div.winfo_reqwidth() + orientation_selector_div.winfo_reqwidth(), height=300)
    setup_div.place(x=padding_x, y=500)

def run_game_loop():
    """
    Starts the game loop.
    """
    # Game loop logic
    pass

def initialize_game(game_screen: tk.Tk, ships_complete_img: list, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Initializes the game by generating ship images and setting up the game screen.
    """
    generate_all_ship_images()
    setup_game_screen(game_screen, ships_complete_img, selected_ship, selected_orientation)

def main():
    """
    Initializes the game by generating ship images and creating the game board.
    Then, it starts the game loop by running the game screen.
    """
    global padding_x
    
    window_menu = create_welcome_screen()
    window_menu.mainloop()

    window_new_game = create_new_game_screen()
    window_new_game.mainloop()

    board_rows = game_data["board_rows"]
    board_columns = game_data["board_columns"]

    game_screen = create_game_screen()
    padding_x = (screen_width // 2) - (game_data["button_width"] * (board_columns // 2 + 0.5))

    selected_ship = tk.StringVar(value=Ship.DESTRUCTOR.name)
    selected_orientation = tk.StringVar(value=Orientation.TOP.name)
    ships_complete_img = []
    
    initialize_game(game_screen, ships_complete_img, selected_ship, selected_orientation)  
    generate_board(game_screen, selected_ship, selected_orientation)

    game_screen.mainloop()

main()