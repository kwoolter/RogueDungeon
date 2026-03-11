import roguedungeon.model as model
import colorama
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console

ROOM_COLOURS = {

    "Shop": Fore.BLACK + Back.YELLOW,
    "Game": Fore.WHITE + Back.BLACK,
    "Room": Fore.BLUE + Back.BLACK,
    "Passageway": Fore.BLACK + Back.MAGENTA,
    "Good" : Fore.BLACK + Back.LIGHTGREEN_EX,
    "Evil": Fore.BLACK + Back.LIGHTRED_EX
}

ROOM_COLOURS_DEFAULT = Fore.WHITE + Back.BLACK

class TextView:
    def __init__(self):
        pass

    @staticmethod
    def initialise():
        colorama.init()
        just_fix_windows_console()


class RoomTextView(TextView):

    def __init__(self, room : model.Room):
        self.room = room

    def print(self):
        print(f"{self.room.name} - {self.room.description}")
        exits = self.room.exits
        print("Exits:", end=" ")
        for exit, is_valid in exits.items():
            if is_valid:
                print(f"{exit.value}",end=" ")

        print()

class MapSquareTextView(TextView):
    def __init__(self, square : model.MapSquare):
        self.square = square

    def print(self):
        room_type_format = ROOM_COLOURS.get(self.square.room.room_type, ROOM_COLOURS_DEFAULT)
        print(f"{Style.BRIGHT}{room_type_format}{self.square.room.name} - {self.square.room.description}{Style.RESET_ALL}")
        for k,v in self.square.exits.items():
            if v.room_id == model.Map.EXIT_NONE:
                pass
            elif v.room_id == model.Map.EXIT_BLOCKED:
                print(f"Exit {k.value} is blocked")
            elif v.room_id == model.Map.EXIT_UNKNOWN:
                print(f"Exit {k.value} is unexplored")
            else:
                print(f"Exit {k.value} leads to {v.name}")





