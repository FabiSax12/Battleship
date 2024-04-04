import tkinter as tk
from PIL import ImageTk, Image
from GUI_game import create_game_screen

# Global variables
board_1 = []
board_2 = []

board_rows = 10
board_colums = 30
button_width = 30

ships = {
    "destructor": ["b1.png"],
    "crucero": ["b21.png", "b22.png"],
    "acorazado": ["b31.png", "b32.png", "b33.png"]
}

ships_Tkinter_images = {
    "destructor": {
        "top": [],
        "right": [],
        "bottom": [],
        "left": []
    },
    "crucero": {
        "top": [],
        "right": [],
        "bottom": [],
        "left": []
    },
    "acorazado": {
        "top": [],
        "right": [],
        "bottom": [],
        "left": []
    },
}

# Style
padding_x = button_width * 4
padding_y = button_width * 2

# GUI
game_screen = create_game_screen(button_width, board_colums, board_rows, padding_x, padding_y)

def generate_all_ship_images():
    for ship in ships.keys():
        for image_path in ships[ship]:
            for orientation in ships_Tkinter_images[ship].keys():
                # Cargar la imagen utilizando PIL
                image = Image.open(f"images/{image_path}")
                image = image.resize((button_width, button_width))
                
                rotated_image = image
                if orientation == "left": rotated_image = image.rotate(180)
                if orientation == "right": rotated_image = image.rotate(0)
                if orientation == "top": rotated_image = image.rotate(90)
                if orientation == "bottom": rotated_image = image.rotate(270)
                
                # Convertir la imagen al formato PhotoImage si aún no ha sido convertida
                if isinstance(rotated_image, Image.Image):
                    photo_image = ImageTk.PhotoImage(rotated_image)
                    # Almacenar la imagen convertida en la lista de imágenes
                    ships_Tkinter_images[ship][orientation].append(photo_image)
    
def on_click_matrix(x, y):
    if x >= board_colums // 2: x -= 15
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

def main():
    # Initialization
    generate_all_ship_images()
    generate_board()

    # Run game screen
    game_screen.mainloop()

main()