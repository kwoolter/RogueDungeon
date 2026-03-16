from pathlib import Path
import pandas as pd
from roguedungeon.model.model_enums import *


class Room:
    def __init__(self,
                 room_id: int,
                 name: str,
                 description: str,
                 room_type: str,
                 rarity: str,
                 min_rank: int,
                 visible: bool,
                 unlock_room_id: int):

        self.room_id = room_id
        self.name = name
        self.description = description
        self.room_type = room_type
        self.rarity = rarity
        self.min_rank = min_rank
        self.visible = visible
        self.unlock_room_id = unlock_room_id
        self.exits = {}

    def __str__(self):
        text = f"{self.name}: Exits "
        for k, v in self.exits.items():
            if v == True:
                text += k.value[0]

        return text

    def add_exit(self, direction: Direction, valid: bool = True):
        self.exits[direction] = valid

    def get_exits(self):
        exits = []

        for direction in Direction:
            if self.exits.get(direction) == True:
                exits.append(direction)

        return exits

    def print(self):
        print(f"{self.room_id}. {self.name} - {self.description} : {self.exits}")


class RoomFactory:
    rooms = None
    UNLOCKS_ROOM = {}
    UNLOCKED_BY_ROOM = {}

    RARITY_TO_INT = {
        "Commonplace": 1,
        "Standard": 2,
        "Unusual": 3,
        "Rare": 4
    }

    INT_TO_RARITY = {
        1:"Commonplace",
        2:"Standard",
        3:"Unusual",
        4:"Rare"
    }

    # Define some column names
    ROOM_VISIBLE_PROPERTY = "Visible"
    EXIT_NORTH = "North"
    EXIT_SOUTH = "South"
    EXIT_EAST = "East"
    EXIT_WEST = "West"
    UNLOCKED_BY = "UnlockedByRoomID"

    EXITS = [EXIT_NORTH, EXIT_SOUTH, EXIT_EAST, EXIT_WEST]

    def __init__(self):
        pass

    @staticmethod
    def load(file_name: str, reload: bool = False):

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

        # Change some columns to booleans
        boolean_columns = [RoomFactory.ROOM_VISIBLE_PROPERTY]
        boolean_columns.append(RoomFactory.EXITS)

        for d in boolean_columns:
            df[d] = df[d] >= 1

        # Add new column that totals the number of exists
        df["ExitCount"] = df[RoomFactory.EXITS].sum(axis=1)

        # Tidy up the column that is used to specify if another room needs to be dealt to reveal this room
        df[RoomFactory.UNLOCKED_BY] = df[RoomFactory.UNLOCKED_BY].fillna(0).astype('int64')

        # Map the rarity text string to an int
        df["RarityInt"] = df["Rarity"].map(RoomFactory.RARITY_TO_INT)

        print(f"{len(df.index)} rooms loaded.")

        # Build maps of which rooms unlock another room
        RoomFactory.UNLOCKED_BY_ROOM = df[df[RoomFactory.UNLOCKED_BY]>0][RoomFactory.UNLOCKED_BY].to_dict()

        print(f"Rooms unlocked by {RoomFactory.UNLOCKED_BY_ROOM}")

        RoomFactory.UNLOCKS_ROOM = {v: k for k, v in RoomFactory.UNLOCKED_BY_ROOM.items()}

        print(f"Room unlocks {RoomFactory.UNLOCKS_ROOM}")





    @staticmethod
    def get_room_info(room_id: int):
        df = RoomFactory.rooms
        if room_id in df.index:
            row = df.loc[room_id]
            room = RoomFactory.row_to_room(room_id, row)
        else:
            room = None
            print(f"Can't find room with ID {room_id}")
        return room

    @staticmethod
    def row_to_room(room_id, row) -> Room:

        room_id = room_id
        name = row["Name"]
        description = row["Description"]
        room_type = row["Type"]
        rarity = row["Rarity"]
        min_rank = row["MinRank"]
        visible = row[RoomFactory.ROOM_VISIBLE_PROPERTY]
        unlock_room_id = row[RoomFactory.UNLOCKED_BY]

        new_room = Room(room_id=room_id,
                        name=name,
                        description=description,
                        room_type=room_type,
                        rarity=rarity,
                        min_rank=min_rank,
                        visible=visible,
                        unlock_room_id=unlock_room_id)

        for direction in Direction:
            is_exit = row[direction.value]
            new_room.add_exit(direction, is_exit)

        return new_room

    @staticmethod
    def get_rooms_by_property(property_name: str, property_value: str) -> list:

        matches = []
        df = RoomFactory.rooms

        if property_name in df.columns:

            q = f"{property_name} == '{property_value}' and {RoomFactory.ROOM_VISIBLE_PROPERTY} == True"
            matched = df.query(q)

            for index, row in matched.iterrows():
                e = RoomFactory.row_to_room(index, row)
                matches.append(e)
        else:
            print(f"Can't find property {property_name} in factory!")

        return matches

    @staticmethod
    def get_matching_rooms(mandatory_exit: Direction,
                           min_exits : int = 1,
                           min_rank: int = 1,
                           max_rank: int = 9,
                           min_rarity: str = "Commonplace",
                           max_rarity: str = "Rare",
                           visible: bool = True) -> list:

        matches = []
        df = RoomFactory.rooms

        # Define the query parameters
        mandatory_exit = mandatory_exit.value
        min_rarity_int = RoomFactory.RARITY_TO_INT[min_rarity]
        max_rarity_int = RoomFactory.RARITY_TO_INT[max_rarity]

        # Build the query
        q = f"Visible == {visible}"
        q += f" and ExitCount >= {min_exits}"
        q += f" and MinRank >= {min_rank}"
        q += f" and MinRank <= {max_rank}"
        q += f" and RarityInt >= {min_rarity_int}"
        q += f" and RarityInt <= {max_rarity_int}"
        q += f" and {mandatory_exit} == True"

        # Run the query
        print(f"Running room query {q}")
        matched = df.query(q)

        # Format the results
        for index, row in matched.iterrows():
            e = RoomFactory.row_to_room(index, row)
            matches.append(e)

        return matches

    @staticmethod
    def get_rooms_by_exit(direction: str) -> list:

        matches = []
        df = RoomFactory.rooms

        if direction in df.columns:

            q = f'{direction} == True and {RoomFactory.ROOM_VISIBLE_PROPERTY} == True'
            matched = df.query(q)

            for index, row in matched.iterrows():
                room = RoomFactory.row_to_room(index, row)
                matches.append(room)
        else:
            print(f"Can't find property {direction} in factory!")

        return matches

    @staticmethod
    def set_room_property(room_id: int, property: str, value):
        room = RoomFactory.get_room_info(room_id)

        if room is not None:
            df = RoomFactory.rooms
            if property in df.columns:
                df.loc[room_id, property] = value
            else:
                print(f"Property {property} is not valid")
        else:
            print(f"Can't find room with ID {room_id}")


def run_tests():
    file_name = "rooms.csv"
    RoomFactory.load(file_name)

    for room_id in range(1, 4):
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

    room_id = 1
    RoomFactory.set_room_property(room_id, "Name", "New Name!!!")
    room = RoomFactory.get_room_info(room_id)
    room.print()

    print("\nMega room query")
    mandatory_exit = Direction.NORTH
    min_exits = 2
    min_rank = 1
    max_rank = 9
    min_rarity = "Commonplace"
    max_rarity = "Rare"
    visible = True

    results = RoomFactory.get_matching_rooms(mandatory_exit,
                                             min_exits,
                                             min_rank, max_rank,
                                             min_rarity, max_rarity,
                                             visible)
    for room in results:
        print(room)


if __name__ == "__main__":
    run_tests()
