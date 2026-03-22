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

RESOURCE_COLOURS = {
    model.Resource.GOLD : Back.YELLOW + Fore.BLACK,
    model.Resource.GEMS : Back.MAGENTA + Fore.BLACK,
    model.Resource.FOOD : Back.BLACK + Fore.RED,
    model.Resource.KEYS : Back.WHITE + Fore.BLACK
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

        print("You have: ", end="")
        for k, v in self.game.resources.items():
            print(f"{RESOURCE_COLOURS[k]} {k.value}:{v} {Style.RESET_ALL}", end=" ")
        print()

        print(f"State: {self.game.state}  |  Rooms: {self.game.rooms}  |  Moves: {self.game.moves}\n")

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

        # If there are some resources here then display them
        if sum(self.square.resources.values())>0:
            print("You can see: ", end="")
            for k,v in self.square.resources.items():
                if v > 0:
                    print(f"{RESOURCE_COLOURS[k]} {k.value}:{v} {Style.RESET_ALL}", end=" ")
            print()

class MapTextView(TextView):
    """ Display a text view of the game map"""
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


    def print2(self):

        if self.map is not None:
            banner = "Rogue Dungeon"
            no_exit = [model.Map.EXIT_BLOCKED, model.Map.EXIT_NONE]

            print(f"\n{Style.BRIGHT}{banner:^36}{Style.RESET_ALL}")

            grid_fgbg = Fore.BLACK + Back.GREEN
            blank_fgbg = Back.BLACK
            room_fgbg = Back.LIGHTWHITE_EX + Fore.BLACK
            header_fgbg1 = Back.LIGHTGREEN_EX + Fore.BLACK
            header_fgbg2 = Back.GREEN + Fore.BLACK
            current_fgbg = Back.LIGHTYELLOW_EX + Fore.BLACK

            # Create a map of exit direction to the character that get printed if the exit is open or closed
            EXIT_TO_TEXT = {
                model.Direction.NORTH: ("  ", f"{Style.RESET_ALL}  "),
                model.Direction.SOUTH: ("  ", f"{Style.RESET_ALL}  "),
                model.Direction.EAST: (" ", f"{Style.RESET_ALL} "),
                model.Direction.WEST: (" ", f"{Style.RESET_ALL} ")
            }

            grid = grid_fgbg + "|"
            grid = ""

            # Build the map header row
            header = "   "
            for x in range(1,6):

                # Alternate colours
                if x % 2 == 0:
                    header_fgbg = header_fgbg1
                else:
                    header_fgbg = header_fgbg2

                header += f"{header_fgbg}   {x}  "

            header += Style.RESET_ALL
            print(header)

            # Loop through each row in the map starting at the top
            for y in range(self.map.max_height - 1, -1, -1):

                # Create 3 empty rows to hold the text
                text = ["" for i in range(3)]

                # Alternate colours
                if y % 2 == 0:
                    header_fgbg = header_fgbg1
                else:
                    header_fgbg = header_fgbg2

                # Start each ro with the value of Y
                for i in range(3):
                    if i == 1:
                        text[i] = header_fgbg + f"{y+1:^3}" + grid
                    else:
                        text[i] = header_fgbg + f"   " + grid

                # Loop through each column in the map
                for x in range(0, self.map.max_width):

                    room_id = self.map.map[x,y]
                    square = self.map.get_map_square_at(x,y)

                    # If this is an empty square fill with blanks
                    if room_id == 0:
                        for i in range(3):
                            text[i] += blank_fgbg + "      " + grid

                    # Otherwise we need to display the square
                    else:
                        if (x,y) == self.map.current_xy:
                            fgbg = current_fgbg
                        else:
                            fgbg = room_fgbg

                        # Loop to create the 3 rows in each map cell
                        for i in range(3):
                            text[i] += ""

                            # If we are on row 0 then this is the North exit
                            if i == 0:
                                direction = model.Direction.NORTH
                                exit = square.exits[direction].room_id
                                o, c = EXIT_TO_TEXT[direction]
                                if exit in no_exit:
                                    x = c
                                elif exit == model.Map.EXIT_UNKNOWN:
                                    x = "??"
                                else:
                                    x = o
                                text[i] += f"{Style.RESET_ALL}  {fgbg}{x}{Style.RESET_ALL}  "

                            # If we are on row 1 then this is the East/West exits
                            elif i == 1:

                                x = ["",""]
                                directions = [model.Direction.WEST, model.Direction.EAST]

                                for i in range(len(directions)):

                                    direction = directions[i]
                                    exit = square.exits[direction].room_id
                                    o, c = EXIT_TO_TEXT[direction]

                                    if exit in no_exit:
                                        x[i] = c
                                    elif exit == model.Map.EXIT_UNKNOWN:
                                        x[i] = "?"
                                    else:
                                        x[i] = o

                                #text[i] += f"{fgbg}{x[0]}{fgbg} {room_id:02} {x[1]}{Style.RESET_ALL}"
                                text[i] += f"{fgbg}{x[0]}{fgbg}    {x[1]}{Style.RESET_ALL}"

                            # if we are on row 2 this is the South exit
                            elif i == 2:

                                direction = model.Direction.SOUTH
                                exit = square.exits[direction].room_id
                                o, c = EXIT_TO_TEXT[direction]
                                if exit in no_exit:
                                    x = c
                                elif exit == model.Map.EXIT_UNKNOWN:
                                    x = "??"
                                else:
                                    x = o

                                text[i] += f"{Style.RESET_ALL}  {fgbg}{x}{Style.RESET_ALL}  "

                        for i in range(3):
                            text[i] += grid

                #row += header_fgbg + f"{y + 1:^3}" + Style.RESET_ALL
                for i in range(3):
                    if i == 1:
                        text[i] += header_fgbg + f"{y + 1:^3}" + Style.RESET_ALL
                    else:
                        text[i] += header_fgbg + f"   " + Style.RESET_ALL

                for i in range(3):
                    print(text[i])

            print(header)

        else:
            print("No map to view")




