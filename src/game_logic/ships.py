import tkinter as tk
from PIL import ImageTk, Image
from enums import Orientation, Ship
from game_data import game_data

ships = {
    Ship.DESTRUCTOR: ["b1.png"],
    Ship.CRUCERO: ["b21.png", "b22.png"],
    Ship.ACORAZADO: ["b31.png", "b32.png", "b33.png"]
}

ships_Tkinter_images = {
    Ship.DESTRUCTOR: {orientation: [] for orientation in Orientation},
    Ship.CRUCERO: {orientation: [] for orientation in Orientation},
    Ship.ACORAZADO: {orientation: [] for orientation in Orientation},
}

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

def place_ship_on_board(board_clicked: list[tk.Button], x: int, y: int, selected_ship: tk.StringVar, selected_orientation: tk.StringVar):
    """
    Handles the click event on the game board.

    Args:
        x (int): The x-coordinate of the clicked position on the game board.
        y (int): The y-coordinate of the clicked position on the game board.
    """
    board_ships = game_data["board_1_ships" if board_clicked == game_data["board_1"] else "board_2_ships"]

    if validate_ship_position(x, y, Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked):

        print_ship_image(Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked, x, y)
        
        board_ships.append((x, y, selected_ship.get(), selected_orientation.get()))