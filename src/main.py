import tkinter                  as tk
import tk_logic.custom_widgets  as custom

from tkinter.font               import Font
from PIL                        import ImageTk, Image
from enum                       import Enum
from enums                      import Orientation, Ship
from game_data                  import ships, game_data, load_game_data
from tk_logic.window_generators import screen_width, create_game_screen, create_new_game_screen, create_welcome_screen
from game_logic.ships           import generate_all_ship_images, posisionate_ship
from game_logic.board           import generate_board, place_buttons_on_board, toggle_board, change_board_buttons_command

# Style
padding_x = None
padding_y = 50

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

def change_player_setup_turn(widget: tk.Widget, new_x, new_y):
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
        lambda: change_player_setup_turn(setup_div, padding_x + (button_width * ((board_columns // 2) + 1)), 500)
    )
    ships_placed_button.place(x=setup_div.winfo_reqwidth() // 2 - 50, y=250)

    setup_div.configure(width=ships_selector_div.winfo_reqwidth() + orientation_selector_div.winfo_reqwidth(), height=300)
    setup_div.place(x=padding_x, y=500)

def start_new_game(window: tk.Tk):
    global padding_x

    window.destroy()
    window_new_game = create_new_game_screen()
    window_new_game.mainloop()

    board_columns = game_data["board_columns"]

    game_screen = create_game_screen()
    padding_x = (screen_width // 2) - (game_data["button_width"] * (board_columns // 2 + 0.5))

    selected_ship = tk.StringVar(value=Ship.DESTRUCTOR.name)
    selected_orientation = tk.StringVar(value=Orientation.TOP.name)
    ships_complete_img = []
    
    generate_all_ship_images()
    setup_game_screen(game_screen, ships_complete_img, selected_ship, selected_orientation)
    generate_board(game_screen, padding_x)
    change_board_buttons_command(lambda board, x, y: posisionate_ship(board, x, y, selected_ship, selected_orientation))

    game_screen.mainloop()

def start_old_game(window: tk.Tk):
    window.destroy()
    load_game_data("mi_partida")

    board_columns = game_data["board_columns"]
    padding_x = (screen_width // 2) - (game_data["button_width"] * (board_columns // 2 + 0.5))

    game_screen = create_game_screen()

    generate_board(game_screen, padding_x)
    place_buttons_on_board(game_data["board_1"], padding_x)
    place_buttons_on_board(game_data["board_2"], padding_x + (game_data["button_width"] * (board_columns // 2 + 1)))
    
    change_board_buttons_command(lambda board,  x, y: print("boom"))

    game_screen.mainloop()

def main():
    window_menu = create_welcome_screen(start_new_game, start_old_game)
    window_menu.mainloop()

if __name__ == "__main__":
    main()