from enum import Enum

class Orientation(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"

class Ship(Enum):
    CRUCERO = "crucero"
    DESTRUCTOR = "destructor"
    ACORAZADO = "acorazado"