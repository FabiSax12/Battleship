from enum import Enum

class GameStage(Enum):
    PLACING_SHIPS = "placing ships"
    PLAYING = "playing"
    END = "end"

class Orientation(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"

class Ship(Enum):
    CRUCERO = "crucero"
    DESTRUCTOR = "destructor"
    ACORAZADO = "acorazado"
    
class Color(Enum):
    WHITE = "#FAF3DD"
    BLACK = "#090302"
    BLUE = "#007EA7"
    RED = "#FB3640"
    GRAY = "#726E75"
    
    def movement_boats(movement: Orientation):
        new c
        match movement:
            case Orientation.TOP:
                
            case Orientation.RIGHT:
                
            case Orientation.BOTTOM:
                
            case Orientation.LEFT:
            
                