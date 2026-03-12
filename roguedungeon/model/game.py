from .rooms import *
from .maps import *
from .card_deck import RoomCardDeck
import random


class RDGame:

    def __init__(self):
        self.map = None
        self.moves = 0
        self.rooms = 0

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

        self.deck.current_x = self.map.current_x
        self.deck.current_y = self.map.current_y
        self.deck.mandatory_exit = direction
        self.deck.max_rank = self.map.current_y + 1
        self.deck.max_rarity = RoomFactory.INT_TO_RARITY[random.randint(1, max(RoomFactory.RARITY_TO_INT.values()))]
        self.deck.max_exits = random.randint(1, 4)

        results = self.deck.get_matching_rooms()

        if len(results) < 3:
            print(f"Deal result only get {len(results)} matching cards")
            rooms = results
        else:
            rooms = random.sample(results, k=3)

        return rooms

    def deal_and_move(self, room_id, direction):

        cx, cy = self.map.current_xy
        x,y = self.map.add_xy(cx, cy, direction)
        self.map.set_room_at(x,y,room_id)
        self.map.move(direction)


    def move(self, direction):
        self.map.move(direction)



