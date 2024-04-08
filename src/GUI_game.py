import tkinter as tk

def create_game_screen(button_width, matrix_cols, matrix_rows, padding_x, padding_y) -> tk.Tk:
    # Graphic Interface
    game_screen = tk.Tk()
    game_screen.title("Battleship")

    # Calculate width and height of the window
    window_width = (button_width * matrix_cols) + (padding_x * 2) + button_width
    window_height = (button_width * matrix_rows) + (padding_y * 2)

    # Get width and height of the screen
    screen_width = game_screen.winfo_screenwidth()
    screen_height = game_screen.winfo_screenheight()

    # Positionate window in center of the screen
    pos_x = round(screen_width/2 - window_width/2)
    pos_y = round(screen_height/2 - window_height/2)
    game_screen.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    return game_screen