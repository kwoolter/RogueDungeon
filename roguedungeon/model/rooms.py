from pathlib import Path
import pandas as pd
from .model_enums import *

class Room:
    def __init__(self,
                 room_id : int,
                 name : str,
                 description : str,
                 room_type : str,
                 rarity : str,
                 min_rank : int,
                 visible : bool):

        self.room_id = room_id
        self.name = name
        self.description = description
        self.room_type = room_type
        self.rarity = rarity
        self.min_rank = min_rank
        self.visible = visible
        self.exits = {}


    def add_exit(self, direction : Direction, valid : bool = True):
        self.exits[direction] = valid

    def print(self):
        print(f"{self.room_id}. {self.name} - {self.description} : {self.exits}")

class RoomFactory:

    rooms = None

    def __init__(self):
        pass

    @staticmethod
    def load(file_name:str, reload : bool = False):

        # Only load if not already loaded and not trying to reload
        if RoomFactory.rooms is not None and reload == False:
            return

        # Create path for the file that we are going to load
        data_folder = Path(__file__).resolve().parent
        file_to_open = data_folder / "data" / file_name

        # Read in the csv file
        RoomFactory.rooms = pd.read_csv(file_to_open)
        df = RoomFactory.rooms
        df.set_index("RoomID", drop=True, inplace=True)

        # Change Visible and Exit direction columns to bools
        for d in ("Visible","North","South","East","West"):
            df[d] = df[d] >= 1

    @staticmethod
    def get_room_info(room_id: int):
        df = RoomFactory.rooms
        row = df.loc[room_id]
        level = RoomFactory.row_to_room(room_id, row)
        return level

    @staticmethod
    def row_to_room(room_id, row) -> Room:

        room_id = room_id
        name = row["Name"]
        description = row["Description"]
        room_type = row["Type"]
        rarity = row["Rarity"]
        min_rank = row["MinRank"]
        visible = row["Visible"]

        new_room = Room(room_id=room_id,
                        name = name,
                        description = description,
                        room_type = room_type,
                        rarity = rarity,
                        min_rank = min_rank,
                        visible = visible)

        for direction in Direction:
            is_exit = row[direction.value]
            new_room.add_exit(direction, is_exit)

        return new_room

    @staticmethod
    def get_rooms_by_property(property_name: str, property_value : str) -> list:

        matches = []
        df = RoomFactory.rooms

        if property_name in df.columns:

            q = f'{property_name} == "{property_value}"'
            matched = df.query(q)

            for index, row in matched.iterrows():
                e = RoomFactory.row_to_room(index, row)
                matches.append(e)
        else:
            print(f"Can't find property {property_name} in factory!")

        return matches

    @staticmethod
    def get_rooms_by_exit(direction: str) -> list:

        matches = []
        df = RoomFactory.rooms

        if direction in df.columns:

            q = f'{direction} == True'
            matched = df.query(q)

            for index, row in matched.iterrows():
                e = RoomFactory.row_to_room(index, row)
                matches.append(e)
        else:
            print(f"Can't find property {direction} in factory!")

        return matches

def run_tests():

    file_name = "rooms.csv"
    RoomFactory.load(file_name)

    for room_id in range(1,4):
        room = RoomFactory.get_room_info(room_id)
        room.print()


    results = RoomFactory.get_rooms_by_property("Rarity", "Unusual")
    for room in results:
        room.print()


    direction = "North"
    print(f"Rooms that have a {direction} exit...")
    results = RoomFactory.get_rooms_by_exit(direction)
    for room in results:
        room.print()





if __name__ == "__main__":
    run_tests()