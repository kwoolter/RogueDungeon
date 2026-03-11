from .rooms import *
from .maps import *
from .card_deck import RoomCardDeck


class RDGame:

    def __init__(self):
        self.map = None

    def initialise(self):

        RoomFactory.load("rooms.csv")
        self.deck = RoomCardDeck()
        self.deck.initialise()

        self.map = Map("Rogue Dungeon")
        self.map.initialise()

    @property
    def current_room_id(self):
        return self.map.current_room_id

    def print(self):

        current_room = RoomFactory.get_room_info(self.current_room_id)
        current_room.print()

    def get_current_room(self):
        return RoomFactory.get_room_info(self.current_room_id)

    def get_current_map_square(self):
        square = self.map.get_map_square_at()
        return square

    def get_adjacent_blank_squares(self):
        square =  self.map.get_map_square_at()
        directions = []
        for k,v in square.exits.items():
            if v.room_id == Map.EXIT_UNKNOWN:
                directions.append(k)

        return directions


    def deal(self, direction):

        rooms = self.deck.get_rooms_by_exit(direction)

        return rooms

    def deal_and_move(self, room_id, direction):

        cx, cy = self.map.current_xy
        x,y = self.map.add_xy(cx, cy, direction)
        self.map.set_room_at(x,y,room_id)
        self.map.move(direction)


    def move(self, direction):
        self.map.move(direction)



