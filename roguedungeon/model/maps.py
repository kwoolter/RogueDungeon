import logging
import numpy as np
import copy

from roguedungeon.model.model_enums import *
from roguedungeon.model.model_exceptions import *
from roguedungeon.model.rooms import Room, RoomFactory


class MapSquare:
    def __init__(self, room_id: int, x: int, y: int):
        self.room_id = room_id
        self.room= None
        self.x = x
        self.y = y

        self.room = None
        self.exits = {}
        self.locks = set()
        self.resources = {}
        self.items = {}

    def initialise(self):
        self.room = RoomFactory.get_room_info(self.room_id)
        self.resources = copy.deepcopy(self.room.resources)


    def get_resource(self, resource : Resource):
        return self.resources.get(resource, 0)

    def set_resource(self, resource : Resource, quantity : int = 0):
        self.resources[resource] = quantity

    def add_resource(self, resource: Resource, quantity: int = 1):
        if resource in self.resources.keys():
            self.resources[resource] += quantity
        else:
            self.resources[resource] = quantity


    def get_item(self, item : Item):
        return self.items.get(item, 0)

    def set_item(self, item : Item, quantity : int = 0):
        self.items[item] = quantity

    def add_item(self, item: Item, quantity: int = 1):
        if item in self.resources.keys():
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def add_exit(self, direction: str, to_room: Room):
        self.exits[direction] = to_room

    def print(self):
        print(f"Room {self.room_id}: {self.room.name}")
        for k, v in self.exits.items():
            print(f"Exit {k.value} leads to {v.name}")

    def lock_exit(self, direction : Direction, lock : bool = True):

        if lock:
            self.locks.add(direction)
            # print(f"Exit {direction} from {self.room.name} is now locked")
        else:
            self.locks.remove(direction)
            # print(f"Exit {direction} from {self.room.name} is now unlocked")


    def is_exit_locked(self, direction : Direction):

        exit = self.exits.get(direction, None)

        if exit is None:
            raise ApplicationException("Exit Locked Check", f"Room {self.room.name} does not have an exit {direction}")
        else:
            locked = direction in self.locks

        return locked


class Map:

    # Define vectors for how x,y coords change based on direction
    DIRECTION_VECTORS = {Direction.NORTH: (0, 1),
                         Direction.SOUTH: (0, -1),
                         Direction.WEST: (-1, 0),
                         Direction.EAST: (1, 0)}

    # Special Game reserved rooms
    EMPTY = 0
    ENTRANCE = 1
    EXIT_END = 99
    EXIT_NONE = 101
    EXIT_BLOCKED = 102
    EXIT_UNKNOWN = EMPTY

    def __init__(self, name: str):

        self.name = name
        self.max_width = 5
        self.max_height = 5
        self.map = None
        self.map_items = {}
        self.moves = 0
        self.rooms = 0
        self.current_xy = (2, 0)
        self._square_cache = {}

    @property
    def current_x(self):
        x,y = self.current_xy
        return x

    @property
    def current_y(self):
        x,y = self.current_xy
        return y

    @property
    def current_room_id(self):
        x, y = self.current_xy
        return self.map[x, y]

    def is_valid_xy(self, x, y):
        if x < 0 or x >= self.max_width or y < 0 or y >= self.max_height:
            return False
        else:
            return True

    def initialise(self):

        # Load the factory of room templates
        RoomFactory.load("rooms.csv")

        # Define a cache for square
        self._square_cache = {}

        # Build an array full of zeros to hold the map details
        self.max_width = 5
        self.max_height = 9
        self.map = np.zeros(self.max_width * self.max_height, dtype=int)
        self.map = self.map.reshape(self.max_width, self.max_height)

        # Populate the map with the entrance and exit squares
        x, y = self.current_xy
        self.set_room_at(x, y, Map.ENTRANCE)
        self.set_room_at(2, 8, Map.EXIT_END)

        # Remove an items from the map
        self.map_items = {}

    def move(self, direction: Direction):
        """ Attempt to move from the current square in the specified direction """

        # Get the details of the current square
        square = self.get_map_square_at()
        destination_room = square.exits.get(direction, None)

        # Get the ID of the room in the specified direction
        if destination_room is not None:
            destination = destination_room.room_id

        # If no exit found in that direction then raise error
        else:
            raise ApplicationException(f"No exit",
                                       f"Room {square.room.name} has no exit to the {direction.value}")

        # If no exit in that direction then raise error
        if destination == Map.EXIT_NONE:
            raise ApplicationException(f"No exit",
                                       f"Room {square.room.name} has no exit to the {direction.value}")

        # Check if there is an exit in the specified direction
        elif destination == Map.EXIT_BLOCKED:
            raise ApplicationException(f"Exit Blocked",
                                       f"Room {square.room.name} exit to the {direction.value} is blocked")

        # Check if a card has been dealt in the specified direction
        elif destination == Map.EXIT_UNKNOWN:
            raise ApplicationException(f"No room drafted",
                                       f"No square has been dealt {direction.value} of {self.current_xy}")
        # All good so let's move
        else:
            x, y = self.current_xy
            new_x, new_y = self.add_xy(x, y, direction)
            self.current_xy = new_x, new_y
            self.moves += 1

        return self.current_xy

    def add_xy(self, x, y, direction: Direction):
        """Calculate a new x,y based on x,y + direction vector"""

        new_x, new_y = self.current_xy
        dx, dy = Map.DIRECTION_VECTORS[direction]
        new_x += dx
        new_y += dy

        if self.is_valid_xy(new_x, new_y) == False:
            raise ApplicationException("New XY out of bounds", f"{new_x},{new_y} out of bounds")

        return new_x, new_y

    def print(self):
        print(f"Map {self.name} - rooms={self.rooms}, moves={self.moves}")
        print(self.map)


    def add_item_at(self, x: int, y: int, item : Item, quantity : int = 1):
        """ Place a quantity of the specified item at an x,y coordinate"""

        # If the specified x,y is in bounds of the map
        if self.is_valid_xy(x, y):
            item_dict = self.map_items.get((x,y),{})
            if item in item_dict.keys():
                item_dict[item] += quantity
            else:
                item_dict[item] = quantity

            self.map_items[(x,y)] = item_dict

            print(f"\tDEBUG: Item {item.value} x {quantity} added at ({x},{y})")
        else:
            raise ApplicationException("Add Item: Room out of bounds", f"{x}, {y} is out of bounds")

    def get_items_at(self, x: int, y: int,):
        map_items = self.map_items.get((x,y),{})
        return map_items

    def set_room_at(self, x: int, y: int, room_id: int):

        # If the specified x,y is in bounds of the map
        if self.is_valid_xy(x, y):

            # Set the room at the specified location
            self.map[x, y] = room_id

            # Increment the number of rooms that have been filled in on the map
            self.rooms += 1

            # Flag the room in the Factory as no longer available
            RoomFactory.set_room_property(room_id, "Visible", False)

            square = self.get_map_square_at(x,y)


        else:
            raise ApplicationException("Set Room: Out of bounds", f"{x}, {y} is out of bounds")

    def get_room_at(self, x: int = None, y: int = None):

        # Default x,y if some values are not specified
        if x is None:
            x, z = self.current_xy
        if y is None:
            z, y = self.current_xy

        # If the x,y is in the bounds of the map...
        if self.is_valid_xy(x, y):

            # Get the ID of the room that is at the x,y location
            room_id = self.map[x, y]

            # If x,y contains a non-empty room...
            if room_id != Map.EMPTY:
                # get the room details from the factory
                room = RoomFactory.get_room_info(room_id)
            else:
                room = None
        else:
            raise ApplicationException("Get room out of bounds", f"{x}, {y} is out of bounds")

        return room

    def get_map_square_at(self, x: int = None, y: int = None):
        ''' Build a MapSquare containing all of the details at the current x,y location on the Map '''

        # Default some values of x,y if they were not specified
        if x is None:
            x, z = self.current_xy
        if y is None:
            z, y = self.current_xy

        # Check that the x,y coordinates are in the bounds of the map
        if self.is_valid_xy(x, y) is True:

            # See is we have already cached the map square at this x,y
            square = self._square_cache.get((x,y), None)

            # Nothing in the cache so we need to create a map square based on the room ID
            if square is None:

                # Create a basic map square
                room_id = self.map[x, y]
                square = MapSquare(room_id, x, y)
                square.initialise()

                # Load up any items that have been added to this square of the map
                map_items = self.map_items.get((x,y),{})
                for k,v in map_items.items():
                    square.add_item(k,v)

                # Store it in the cache if it is a real room
                if room_id != Map.EXIT_UNKNOWN:
                    self._square_cache[(x,y)] = square

            # Add the exits to the map square even if we found it in the cache so we get the latest state
            for k, v in square.room.exits.items():
                # If no exit for this direction then add an NO EXIT room to the square
                if not v:
                    square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_NONE))
                else:

                    # Get the coordinates of the square for this exit
                    dx, dy = Map.DIRECTION_VECTORS[k]
                    rx = x + dx
                    ry = y + dy

                    # If the adjacent square in bounds?
                    if self.is_valid_xy(rx, ry) is True:

                        adj_room_id = self.map[rx][ry]

                        # If the adjacent square is 0 then no card has been dealt here yet
                        if adj_room_id == Map.EXIT_UNKNOWN:
                            square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_UNKNOWN))

                        # else there is a dealt card...
                        else:

                            # Get the details of the room template from the Factory
                            adj_room = RoomFactory.get_room_info(adj_room_id)

                            # Check if the adjacent card's opposite exit lines up with this card?
                            opp_exist = DIRECTION_REVERSE[k]
                            if adj_room.exits.get(opp_exist, False) == True:
                                square.add_exit(k, adj_room)

                            # If it doesn't line up then it is blocked
                            else:
                                square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_BLOCKED))

                    # If not in bounds then show as blocked
                    else:
                        square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_BLOCKED))

        else:
            raise ApplicationException("Get square out of bounds", f"{x}, {y} is out of bounds")

        return square


def test():
    logging.basicConfig(level=logging.INFO)

    my_map = Map("Test Map")
    my_map.initialise()
    my_map.print()

    map_square = my_map.get_map_square_at()
    map_square.print()


if __name__ == "__main__":
    test()
