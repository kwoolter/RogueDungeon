import roguedungeon.model as model
import numpy as np
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

class GameTextView(TextView):
    def __init__(self, game : model.RDGame):
        super().__init__()
        self.game = game

    def print(self):
        banner = self.game.name
        print(f"\n{Style.BRIGHT}{banner}{Style.RESET_ALL}")
        print(f"State: {self.game.state}")
        print(f"Rooms: {self.game.rooms}")
        print(f"Moves: {self.game.moves}")

class RoomTextView(TextView):

    def __init__(self, room : model.Room):
        super().__init__()
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
        super().__init__()
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

class MapTextView(TextView):
    def __init__(self, map : model.Map):
        super().__init__()
        self.map = map

    def print(self):
        if self.map is not None:
            banner = "Rogue Dungeon"
            print(f"\n{Style.BRIGHT}{banner:^32}{Style.RESET_ALL}")

            grid_fgbg = Fore.BLACK + Back.GREEN
            blank_fgbg = Back.BLACK
            room_fgbg = Back.LIGHTWHITE_EX + Fore.BLACK
            header_fgbg = Back.LIGHTGREEN_EX + Fore.BLACK
            current_fgbg = Back.LIGHTYELLOW_EX + Fore.BLACK

            header = "   " + header_fgbg
            for x in range(1,6):
                header += f"|{x:^4}"
            header += "|" + Style.RESET_ALL

            print(header)
            for y in range(self.map.max_height - 1, -1, -1):
                row = header_fgbg + f"{y+1:^3}" + grid_fgbg + "|"
                for x in range(0, self.map.max_width):

                    room_id = self.map.map[x,y]

                    if room_id == 0:
                        row += blank_fgbg + "    " + grid_fgbg + "|"
                    else:
                        if (x,y) == self.map.current_xy:
                            row += current_fgbg
                        else:
                            row += room_fgbg
                        row += f"{f'{room_id:02}':^4}" + grid_fgbg + "|"

                row += header_fgbg + f"{y + 1:^3}" + Style.RESET_ALL
                print(row)
            print(header)

        else:
            print("No map to view")






