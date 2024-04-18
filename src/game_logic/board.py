import tkinter as tk
from game_data import game_data


def place_buttons_on_board(board: list, placement_x: int = None, padding_x: int = 0, padding_y: int = 50):
    """
    Position the buttons on the game screen based on the provided board and placement coordinates.

    Args:
        board (list): The game board containing the buttons.
        placement_x (int, optional): The x-coordinate where the buttons will be placed on the screen.
            If not provided, the default behavior is to start at the `padding_x`.
        padding_x (int, optional): The x-coordinate padding from the left edge of the window.
            Defaults to 0.
        padding_y (int, optional): The y-coordinate padding from the top edge of the window.
            Defaults to 50.
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

def toggle_board():
    """
    Toggles the state of all buttons on both boards.
    """
    for row in board_1:
        for btn in row:
            state = btn["state"]
            btn.config(state="normal" if state == "disabled" else "disabled")

    for row in board_2:
        for btn in row:
            state = btn["state"]
            btn.config(state="normal" if state == "disabled" else "disabled")
            
def clean_board(board):
    print("borrando")
    for row in board:
        for button in row:
            button.config(image = '')
            
def generate_board(window: tk.Tk, padding_x: int = 0):
    """
    Generates the game boards, initializes buttons, and places them on the game screen.

    Args:
        window (tk.Tk): The Tkinter window where the game boards will be placed.
        padding_x (int): The padding to adjust the horizontal position of the boards.

    This function creates two game boards, initializes buttons for each cell, and then places these buttons on the game screen.
    """
    global board_1, board_2

    board_rows = game_data["board_rows"]
    board_columns = game_data["board_columns"]

    # Create a 2D list of buttons representing the game board
    game_board = [
        [
            tk.Button(
                window,
                command=None, 
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

    # Divide the game board into two separate boards
    board_1 = [game_board[row][0 : board_columns // 2] for row in range(board_rows)]
    board_2 = [game_board[row][board_columns // 2:] for row in range(board_rows)]

    # Update game data with the new board configurations
    game_data["board_1"] = board_1
    game_data["board_2"] = board_2

    # Toggle the board for the current player's turn
    toggle_board()

    # Place buttons on the game screen for each board
    place_buttons_on_board(board_1, padding_x)
    place_buttons_on_board(board_2, padding_x + (game_data["button_width"] * (board_columns // 2 + 1)))

def enable_board(board: list):
    """
    Enable all buttons on the specified board.

    Args:
        board: The board containing buttons to be enabled.
    """
    for row in board:
        for btn in row:
            btn.config(state="normal")

def change_board_buttons_command(new_action: callable):
    """
    Change the command of each button on the game board.

    Args:
        new_action: The new command to be executed when a button is clicked.
    """
    board_1 = game_data["board_1"]
    board_2 = game_data["board_2"]

    for i, row in enumerate(board_1):
        for j, btn in enumerate(row):
            btn.config(command=lambda x=j, y=i, board=board_1: new_action(board, x, y))

    for i, row in enumerate(board_2):
        for j, btn in enumerate(row):
            btn.config(command=lambda x=j, y=i, board=board_2: new_action(board, x, y))

