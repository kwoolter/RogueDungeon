import roguedungeon.model as model
import colorama
from colorama import Fore, Back, Style

class TextView:
    def __init__(self):
        pass

    @staticmethod
    def initialise():
        colorama.init()


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
        print(f"{Style.BRIGHT}{self.square.room.name} - {self.square.room.description}{Style.RESET_ALL}")
        for k,v in self.square.exits.items():
            if v.room_id != model.Map.EXIT_NONE:
                print(f"Exit {k.value} leads to {v.name}")





