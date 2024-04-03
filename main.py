import tkinter as tk
from GUI_game import create_game_screen

# Global variables
game_board = []
button_width = 40
matrix_rows = 10
matrix_cols = 20
padding_x = button_width * 4
padding_y = button_width * 2

# GUI
game_screen = create_game_screen(button_width, matrix_cols, matrix_rows, padding_x, padding_y)

def on_click_matrix(x, y):
    print((x, y))

def colocate_buttons_on_screen():
    btnX = padding_x
    btnY = padding_y

    for row in game_board:
        for btn in row:
            btn.place(x=btnX,y=btnY, width=button_width, height=button_width)
            btnX += button_width
        btnX = padding_x
        btnY += button_width

def generate_board(x: int, y: int):
    global game_board

    game_board = [
        [
            tk.Button(game_screen, command=lambda x=col, y=row: on_click_matrix(x, y))
            for col in range(x)
        ] 
        for row in range(y)
    ]

    colocate_buttons_on_screen()

def main():
    # Initialization
    generate_board(20, 10)

    # Run game screen
    game_screen.mainloop()