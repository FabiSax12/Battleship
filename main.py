import tkinter as tk
from GUI_game import create_game_screen

# Global variables
board_1 = []
board_2 = []

board_rows = 10
board_colums = 30
button_width = 30

# Style
padding_x = button_width * 4
padding_y = button_width * 2

# GUI
game_screen = create_game_screen(button_width, board_colums, board_rows, padding_x, padding_y)

def on_click_matrix(x, y):
    if x >= 15: x -= 15
    print((x, y))

def colocate_buttons_on_screen(board: list, placement_x: int):
    btnX = placement_x
    btnY = padding_y
    current_x = 0

    for row in board:
        for btn in row:
            if current_x == board_colums // 2: btnX += button_width
            btn.place(x=btnX, y=btnY, width=button_width, height=button_width)
            btnX += button_width
            current_x += 1

        btnX = placement_x
        btnY += button_width
        current_x = 0

def generate_board():
    global board_1
    global board_2

    game_board = [
        [
            tk.Button(game_screen, 
                      command=lambda x=col, y=row: on_click_matrix(x, y),
                      background="lightBlue", 
                      activebackground="lightBlue",
                    #   border="blue",
                      borderwidth=1,
                      relief="solid",
                      compound="center",
                      cursor="crosshair"
                    )

            for col in range(board_colums)
        ] 
        for row in range(board_rows)
    ]

    board_1 = game_board[ : 15]
    board_2 = game_board[15 : ]

    colocate_buttons_on_screen(board_1, padding_x)
    colocate_buttons_on_screen(board_2, padding_x + button_width * (board_colums / 2 + 1))

def main():
    # Initialization
    generate_board()

    # Run game screen
    game_screen.mainloop()

main()