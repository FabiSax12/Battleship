import tkinter as tk
from PIL import ImageTk, Image
from enums import Orientation, Ship
from game_data import game_data
from game_logic.board import toggle_board

ships_limit = {
    Ship.DESTRUCTOR: 6,
    Ship.CRUCERO: 4,
    Ship.ACORAZADO: 2
}

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

def place_ship_on_board(board_clicked: list[tk.Button], x: int, y: int, selected_ship: tk.StringVar, selected_orientation: tk.StringVar, update_frame, frame_to_update):
    """
    Handles the click event on the game board.

    Args:
        x (int): The x-coordinate of the clicked position on the game board.
        y (int): The y-coordinate of the clicked position on the game board.
    """
    board_ships = game_data["board_1_ships" if board_clicked == game_data["board_1"] else "board_2_ships"]
    player = 0 if board_clicked == game_data["board_1"] else 1

    if validate_ship_position(x, y, Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked):
        if game_data["players"][player]["ships"][Ship[selected_ship.get()].value] < ships_limit[Ship[selected_ship.get()]]:
            game_data["players"][player]["ships"][Ship[selected_ship.get()].value] += 1
            print_ship_image(Ship[selected_ship.get()], Orientation[selected_orientation.get()], board_clicked, x, y)
            board_ships.append([x, y, selected_ship.get(), selected_orientation.get(), [False for _ in range(len(ships[Ship[selected_ship.get()]]))]])

            for widget in frame_to_update[player].winfo_children():
                widget.destroy()
            update_frame(frame_to_update[player], player).pack()

def validate_ships_collision(wanted_x: int, wanted_y: int, placed_ships: list, ship_index: int) -> bool:
    """
    Validate if moving a ship to the specified coordinates causes a collision with other ships.

    Args:
        wanted_x (int): The x-coordinate of the desired position.
        wanted_y (int): The y-coordinate of the desired position.
        placed_ships (list): The list of currently placed ships.
        ship_index (int): The index of the ship being moved.

    Returns:
        bool: True if there is a collision, False otherwise.
    """
    for i, ship_data in enumerate(placed_ships):
        if i == ship_index:
            continue

        x = ship_data[0]
        y = ship_data[1]
        ship_length = len(ships[Ship[ship_data[2]]])
        orientation = Orientation[ship_data[3]]

        for j in range(ship_length):
            x = ship_data[0]
            y = ship_data[1]
            if orientation == Orientation.TOP:
                y += j
            elif orientation == Orientation.BOTTOM:
                y -= j
            elif orientation == Orientation.LEFT:
                x += j
            elif orientation == Orientation.RIGHT:
                x -= j

            if x == wanted_x and y == wanted_y:
                return True

    return False

def move_ships(placed_ships: list[int, int, str, str]):
    for i, ship_data in enumerate(placed_ships):

        if ship_data[4].count(True) >= 1: continue # If the ship has been hit, don't move it

        x = placed_ships[i][0]
        y = placed_ships[i][1]
        ship = placed_ships[i][2]
        orientation = placed_ships[i][3]
        
        if orientation == Orientation.TOP.name:
            if y == 0 or validate_ships_collision(x, y - 1, placed_ships, i): 
                placed_ships[i][3] = Orientation.BOTTOM.name
                placed_ships[i][1] = y + (len(ships[Ship[ship]]) - 1) if y + (len(ships[Ship[ship]]) - 1) < game_data["board_rows"] else y
            else:
                placed_ships[i][1] = y - 1
            
        elif orientation == Orientation.BOTTOM.name:
            if y == game_data["board_rows"] - 1 or validate_ships_collision(x, y + 1, placed_ships, i):
                placed_ships[i][3] = Orientation.TOP.name
                placed_ships[i][1] = y - (len(ships[Ship[ship]]) - 1) if y - (len(ships[Ship[ship]]) - 1) >= 0 else y
            else:
                placed_ships[i][1] = y + 1
                
        elif orientation == Orientation.LEFT.name:
            if x == 0 or validate_ships_collision(x - 1, y, placed_ships, i):
                placed_ships[i][3] = Orientation.RIGHT.name
                placed_ships[i][0] = x + (len(ships[Ship[ship]]) - 1) if x + (len(ships[Ship[ship]]) - 1) < game_data["board_columns"] // 2 else x
            else:
                placed_ships[i][0] = x - 1
                
        elif orientation == Orientation.RIGHT.name:
            if x == game_data["board_columns"] // 2 - 1 or validate_ships_collision(x + 1, y, placed_ships, i):
                placed_ships[i][3] = Orientation.LEFT.name
                placed_ships[i][0] = x - (len(ships[Ship[ship]]) - 1) if x - (len(ships[Ship[ship]]) - 1) >= 0 else x
            else:
                placed_ships[i][0] = x + 1

def validate_shot(x: int, y: int, board: list, update_frame, frames_to_update):
    ships_list = game_data["board_1_ships"] if board == game_data["board_1"] else game_data["board_2_ships"]


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

            if moved_x == x and moved_y == y:
                frame = frames_to_update[0 if board == game_data["board_1"] else 1]
                ship_data[4][i] = True
                board[y][x].config(background="red")

                x = x if board == game_data["board_1"] else x + game_data["board_columns"] // 2
                game_data["buttons_hit"].append([x, y])

                if ship_data[4].count(False) == 0:
                    game_data["players"][0 if board == game_data["board_1"] else 1]["ships"][ship.value] -= 1
                    for widget in frame.winfo_children():
                        widget.destroy()
                    update_frame(frame, 0 if board == game_data["board_1"] else 1).pack()

    move_ships(game_data["board_1_ships"])
    move_ships(game_data["board_2_ships"])
    toggle_board()
    game_data["turn"] = 2 if game_data["turn"] == 1 else 1

