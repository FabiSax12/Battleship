import tkinter as tk
from PIL import ImageTk, Image
from GUI_game import create_game_screen
from enums import *

# Global variables
board_1 = []
board_2 = []

board_rows = 10
board_colums = 30 
button_width = 30

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

# Style
padding_x = button_width * 4
padding_y = button_width * 2

# GUI
game_screen = create_game_screen(button_width, board_colums, board_rows, padding_x, padding_y)

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

def on_click_matrix(x: int, y: int):
    """
    Handles the click event on the game board.

    Args:
        x (int): The x-coordinate of the clicked position on the game board.
        y (int): The y-coordinate of the clicked position on the game board.
    """
    if x >= board_colums // 2:
        x -= board_colums // 2

    print_ship_image(Ship.ACORAZADO, Orientation.TOP, board_1, x, y)
    
def colocate_buttons_on_screen(board: list, placement_x: int):
    """
    Positions the buttons on the game screen based on the provided board and placement coordinates.

    Args:
        board (list): The game board containing the buttons.
        placement_x (int): The x-coordinate where the buttons will be placed on the screen.
    """
    x_offset = button_width if len(board[0]) > board_colums // 2 else 0
    y_offset = button_width

    for row in range(len(board)):
        for col in range(len(board[row])):
            btn = board[row][col]
            x_pos = placement_x + col * button_width + (col // (board_colums // 2)) * x_offset
            y_pos = padding_y + row * button_width
            btn.place(x=x_pos, y=y_pos, width=button_width, height=button_width)

def generate_board():
    """
    Generates the game boards, initializes buttons, and places them on the game screen.

    This function creates two game boards, initializes buttons for each cell, and then places these buttons on the game screen.
    """
    global board_1
    global board_2

    game_board = [
        [
            tk.Button(game_screen, 
                      command=lambda x=col, y=row: on_click_matrix(x, y),
                      background="lightBlue", 
                      activebackground="lightBlue",
                      borderwidth=1,
                      relief="solid",
                      compound="center",
                      cursor="crosshair"
                    )

            for col in range(board_colums)
        ] 
        for row in range(board_rows)
    ]

    board_1 = [game_board[row][0 : 15] for row in range(board_rows)]
    board_2 = [game_board[row][15:   ] for row in range(board_rows)]

    colocate_buttons_on_screen(board_1, padding_x)
    colocate_buttons_on_screen(board_2, padding_x + button_width * (board_colums / 2 + 1))

def generate_all_ship_images():
    """
    Generates images of all ships in all orientations.

    This function iterates over all ships and orientations, loads their respective images, resizes them to match the button size,
    and rotates them based on the orientation. It then converts the rotated images into PhotoImage objects and stores them in the
    ships_Tkinter_images dictionary.
    """
    for ship in ships.keys():
        for orientation in ships_Tkinter_images[ship].keys():
            for image_path in ships[ship]:
                image = Image.open(f"images/{image_path}")
                image = image.resize((button_width, button_width))
                
                if orientation == Orientation.LEFT:     rotated_image = image.rotate(180)
                elif orientation == Orientation.RIGHT:  rotated_image = image.rotate(0)
                elif orientation == Orientation.TOP:    rotated_image = image.rotate(90)
                elif orientation == Orientation.BOTTOM: rotated_image = image.rotate(270)
                
                if isinstance(rotated_image, Image.Image):
                    photo_image = ImageTk.PhotoImage(rotated_image)
                    ships_Tkinter_images[ship][orientation].append(photo_image)

def main():
    """
    Initializes the game by generating ship images and creating the game board.
    Then, it starts the game loop by running the game screen.
    """

    # Initialization
    generate_all_ship_images()
    generate_board()

    # Run game screen
    game_screen.mainloop()

main()