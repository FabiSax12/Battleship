import tkinter as tk
from game_data import *

def center_window(window: tk.Tk, window_width: int, window_height: int) -> list:
    # Get width and height of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Positionate window in center of the screen
    pos_x = round(screen_width/2 - window_width/2)
    pos_y = round(screen_height/2 - window_height/2)

    return [pos_x, pos_y]

def create_game_screen(padding_x, padding_y) -> tk.Tk:
    # Graphic Interface
    game_screen = tk.Tk()
    game_screen.title("Battleship")

    # Calculate width and height of the window
    window_width = int((button_width * board_colums) + (padding_x * 2) + button_width)
    window_height = int((button_width * board_rows) + (padding_y * 2))

    [pos_x, pos_y] = center_window(game_screen, window_width, window_height)

    game_screen.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    return game_screen

def create_setup_screen(player, padding_x = 0, padding_y = 0) -> tk.Tk:
    # Graphic Interface
    setup_screen = tk.Tk()
    setup_screen.title(player["nickname"])

    window_width = (button_width * board_colums // 2) + (padding_x * 2)
    window_height = (button_width * board_rows // 2) + (padding_y * 2)

    [pos_x, pos_y] = center_window(setup_screen, window_width, window_height)

    setup_screen.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    return setup_screen