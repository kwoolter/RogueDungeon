from .rooms import *
from .maps import *
from .card_deck import RoomCardDeck


class RDGame:

    def __init__(self):
        self.map = None

    def initialise(self):

        RoomFactory.load("rooms.csv")
        self.deck = RoomCardDeck()

        self.map = Map("Rogue Dungeon")
        self.map.initialise()


        self.current_room_id = 1
        self.current_rank = 1

    def print(self):

        current_room = RoomFactory.get_room_info(self.current_room_id)
        current_room.print()

    def get_current_room(self):
        return RoomFactory.get_room_info(self.current_room_id)

    def get_current_map_square(self):
        square = self.map.get_map_square_at()
        return square


    def deal(self, direction):

        rooms = []



        return rooms

