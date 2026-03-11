import roguedungeon.model as model

class RoomTextView:

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

class MapSquareTextView:
    def __init__(self, square : model.MapSquare):
        self.square = square

    def print(self):
        print(f"Room {self.square.room_id}: {self.square.room.name}")
        for k,v in self.square.exits.items():
            print(f"Exit {k.value} leads to {v.name}")





