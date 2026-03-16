from .rooms import *
from .maps import *
from .card_deck import RoomCardDeck
import random


class RDGame:

    # Define game states
    STATE_LOADED = "Loaded"
    STATE_PLAYING = "Playing"
    STATE_VICTORY = "Victory"
    STATE_GAME_OVER = "Game Over"


    def __init__(self, name : str):
        self.name = name
        self.map = None
        self.state = RDGame.STATE_LOADED

    @property
    def rooms(self):
        if self.map is not None:
            return self.map.rooms
        else:
            return 0

    @property
    def moves(self):
        if self.map is not None:
            return self.map.moves
        else:
            return 0

    def initialise(self):

        RoomFactory.load("rooms.csv")
        self.deck = RoomCardDeck()
        self.deck.initialise()

        self.map = Map("Rogue Dungeon")
        self.map.initialise()

        self.state = RDGame.STATE_PLAYING

    @property
    def current_room_id(self):
        return self.map.current_room_id

    def print(self):
        print(f"{self.name} ({self.state})")

        if self.state == RDGame.STATE_PLAYING:
            current_room = RoomFactory.get_room_info(self.current_room_id)
            current_room.print()

    def get_current_room(self):
        return RoomFactory.get_room_info(self.current_room_id)

    def get_current_map_square(self):
        square = self.map.get_map_square_at()
        return square

    def get_adjacent_blank_squares(self):

        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that this time", f"{self.name} game in state {self.state}")

        square =  self.map.get_map_square_at()
        directions = []
        for k,v in square.exits.items():
            if v.room_id == Map.EXIT_UNKNOWN:
                directions.append(k)

        return directions


    def deal(self, direction):

        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that at this time", f"{self.name} game in state {self.state}")

        self.deck.current_x = self.map.current_x
        self.deck.current_y = self.map.current_y
        self.deck.mandatory_exit = direction
        self.deck.max_rank = self.map.current_y + 1
        self.deck.max_rarity = RoomFactory.INT_TO_RARITY[random.randint(1, max(RoomFactory.RARITY_TO_INT.values()))]
        self.deck.max_exits = random.randint(1, 4)

        self.pre_deal_processing()

        results = self.deck.get_matching_rooms()

        if len(results) < 3:
            print(f"Deal result only get {len(results)} matching cards")
            rooms = results
        else:
            rooms = random.sample(results, k=3)

        return rooms

    def pre_deal_processing(self):
        """Put any logic here that you want to kick-in before the deal is made"""
        pass

    def post_deal_processing(self):
        """Put any logic here that you want to kick-in once a new room card has been selected """

        # Get details of teh current room
        room_id = self.map.current_room_id
        room_trigger = RoomFactory.get_room_info(room_id)

        # Process rooms that when dealt make other rooms visible
        unlocks_room_id = RoomFactory.UNLOCKS_ROOM.get(room_id, 0)
        if unlocks_room_id > 0:
            RoomFactory.set_room_property(unlocks_room_id, RoomFactory.ROOM_VISIBLE_PROPERTY, True)
            room = RoomFactory.get_room_info(unlocks_room_id)
            print(f"You explored {room_trigger.name} which makes {room.name} available")


    def deal_and_move(self, room_id, direction):

        cx, cy = self.map.current_xy
        x,y = self.map.add_xy(cx, cy, direction)
        self.map.set_room_at(x,y,room_id)
        self.map.move(direction)
        self.post_deal_processing()


    def move(self, direction):
        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that at this time", f"{self.name} game in state {self.state}")

        self.map.move(direction)

        if self.map.current_room_id == Map.EXIT_END:
            self.state = RDGame.STATE_VICTORY

    def end(self):
        self.state = RDGame.STATE_GAME_OVER



