import logging
import numpy as np

from .model_enums import *
from .rooms import Room, RoomFactory


class MapSquare:
    def __init__(self, room_id: int, x : int, y: int):

        self.room_id = room_id
        self.x = x
        self.y = y

        self.room = None
        self.exits = {}

    def initialise(self):
        pass

    def add_exit(self, direction : str, to_room : Room):
        self.exits[direction] = to_room

    def print(self):
        print(f"Room {self.room_id}: {self.room.name}")
        for k,v in self.exits.items():
            print(f"Exit {k.value} leads to {v.name}")


class Map:

    DIRECTION_VECTORS = {Direction.NORTH: (0, 1),
                         Direction.SOUTH: (0, -1),
                         Direction.WEST: (-1, 0),
                         Direction.EAST: (1, 0)}

    EXIT_NONE = 98
    EXIT_BLOCKED = 99
    EXIT_UNKNOWN = 100

    def __init__(self, name:str):
        self.name = name
        self.map = None
        self.current_xy = (2,0)

    def is_valid_xy(self, x, y):
        if x < 0 or x >= self.max_width or y < 0 or y >= self.max_height:
            raise False
        else:
            return True

    def initialise(self):

        RoomFactory.load("rooms.csv")

        self.max_width = 5
        self.max_height = 9
        self.map = np.zeros(self.max_width * self.max_height, dtype=int)
        self.map = self.map.reshape(self.max_width, self.max_height)

        start_room = 1
        self.map[self.current_xy] = start_room


    def move(self, direction : Direction):

        new_x, new_y = self.current_xy
        dx, dy = Map.DIRECTION_VECTORS[direction]
        new_x += dx
        new_y += dy

        if self.is_valid_xy(new_x, new_y):
            self.current_xy = (new_x, new_y)

        return self.current_xy




    def print(self):
        print(f"Map {self.name}")
        print(self.map)



    def get_room_at(self, x : int = None, y: int = None):
        if x is None:
            x,y = self.current_xy
        elif y is None:
            z,y = self.current_xy

        room_id = self.map[x,y]
        if room_id > 0:
            room = RoomFactory.get_room_info(room_id)
        else:
            room = None
        return room

    def get_map_square_at(self, x : int = None, y: int = None):

        if x is None:
            x,y = self.current_xy
        elif y is None:
            z,y = self.current_xy

        if self.is_valid_xy(x,y) is True:
            room_id = self.map[x,y]
            square = MapSquare(room_id, x, y)
            room = RoomFactory.get_room_info(room_id)
            square.room = room

            for k,v in room.exits.items():
                if v == False:
                    square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_NONE))
                else:

                    dx,dy = Map.DIRECTION_VECTORS[k]
                    rx = x + dx
                    ry = y + dy

                    # If the adjacent square in bounds?
                    if self.is_valid_xy(rx,ry) is True:
                        adj_room_id = self.map[rx][ry]

                        # If the adjacent square is 0 then no card has been dealt here yet
                        if adj_room_id == 0:
                            square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_UNKNOWN))
                        # else there is a dealt card...
                        else:
                            adj_room = RoomFactory.get_room_info(adj_room_id)
                            opp_exist = DIRECTION_REVERSE[k]
                            # Check if the adjacent cards exit lines up with thos card?
                            if adj_room.exits.get(opp_exist, False) == True:
                                square.add_exit(k, adj_room)
                            # If it doesn't line up then it is blocked
                            else:
                                square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_BLOCKED))

                    else:
                        square.add_exit(k, RoomFactory.get_room_info(Map.EXIT_BLOCKED))




        else:
            square = None



        return square



def test():

    logging.basicConfig(level=logging.INFO)

    my_map = Map("Test Map")
    my_map.initialise()
    my_map.print()

    map_square =  my_map.get_map_square_at()
    map_square.print()




if __name__ == "__main__":
    test()