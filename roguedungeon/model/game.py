from .rooms import *
from .maps import *
from .card_deck import RoomCardDeck
import random
import collections
from .events import *

class EventQueue:
    def __init__(self):
        self.events = collections.deque()

    def add_event(self, new_event: Event):
        self.events.append(new_event)

    def pop_event(self):
        return self.events.pop()

    def size(self):
        return len(self.events)

    def print(self):
        for event in self.events:
            print(event)

class RDGame:
    # Define game states
    STATE_LOADED = "Loaded"
    STATE_PLAYING = "Playing"
    STATE_VICTORY = "Victory"
    STATE_GAME_OVER = "Game Over"

    def __init__(self, name: str):
        self.name = name
        self.map = None
        self.state = RDGame.STATE_LOADED
        self.resources = {}
        self.events = EventQueue()

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
        """ Get the game to be ready to play """

        # Load all the room templates
        RoomFactory.load("rooms.csv")

        # Initialise the deck of room cards
        self.deck = RoomCardDeck()
        self.deck.initialise()

        # Create the dungeon map
        self.map = Map(self.name)
        self.map.initialise()

        # Initialise the player's inventory of resources
        self.resources = {resource: 0 for resource in Resource}

        # Change the game state to show we are ready to go
        self.state = RDGame.STATE_PLAYING



    @property
    def current_room_id(self):
        return self.map.current_room_id

    def print(self):
        print(f"{self.name} ({self.state})")

        if self.state == RDGame.STATE_PLAYING:
            current_room = RoomFactory.get_room_info(self.current_room_id)
            current_room.print()

    def get_next_event(self) -> Event:
        """
        Get the next event in the Model's event queue.

        :return:The next event in the event queue

        """
        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()
        return next_event

    def get_current_room(self):
        return RoomFactory.get_room_info(self.current_room_id)

    def get_current_map_square(self):
        square = self.map.get_map_square_at()

        return square

    def get_square_resources(self):
        square = self.map.get_map_square_at()
        return list(square.resources.keys())

    def take_resource(self, resource: Resource):
        """Take all the specified resource at the current room and add it to your inventory"""

        # Get the current square and see how much of the specified resource there is
        square = self.get_current_map_square()
        resource_quantity = square.resources.get(resource, 0)

        # If there are some of the specified resources here...
        if resource_quantity > 0:
            # Add the resources to your inventory
            self.resources[resource] += resource_quantity
            # Zap the resources from the square
            del square.resources[resource]

            # Print what just happened
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_TAKE_RESOURCE,
                                        description=f"You take {resource_quantity} {resource} from {square.room.name}"))

        else:
            raise ApplicationException("", f"There is no {resource.value} here")

    def get_adjacent_blank_squares(self):

        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that this time", f"{self.name} game in state {self.state}")

        # Get the current square
        square = self.map.get_map_square_at()

        # Loop through the square's exists and record which ones are unexplored
        directions = []
        for k, v in square.exits.items():
            if v.room_id == Map.EXIT_UNKNOWN:
                directions.append(k)

        return directions

    def deal(self, direction):

        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that at this time", f"{self.name} game in state {self.state}")

        # Set all the game parameters that go into the dealing logic
        self.deck.current_x = self.map.current_x
        self.deck.current_y = self.map.current_y
        self.deck.mandatory_exit = direction
        self.deck.max_rank = self.map.current_y + 1
        self.deck.max_rarity = RoomFactory.INT_TO_RARITY[random.randint(1, max(RoomFactory.RARITY_TO_INT.values()))]
        self.deck.max_exits = random.randint(1, 4)

        # Do anything that needs doing before we go ahead and deal
        self.pre_deal_processing()

        # Deal some cards
        results = self.deck.get_matching_rooms()

        # If we got 3 or less results then just use these
        if len(results) <= 3:
            print(f"Deal result only get {len(results)} matching cards")
            rooms = results
        # Else sample 3 random cards
        else:
            rooms = random.sample(results, k=3)

        return rooms

    def pre_deal_processing(self):
        """Put any logic here that you want to kick-in before the deal is made"""
        pass

    def post_deal_processing(self):
        """Put any logic here that you want to kick-in once a new room card has been selected """

        # Get details of the current room
        room_id = self.map.current_room_id
        room_trigger = RoomFactory.get_room_info(room_id)

        # If we have got to the end of the dungeon then set the game state to victory
        if room_id == Map.EXIT_END:
            self.state = RDGame.STATE_VICTORY
            self.events.add_event(Event(type=Event.STATE,
                                        name=Event.STATE_VICTORY,
                                        description=f"Victory! You completed the Rogue Dungeon in {self.moves} move."))

        # Process rooms that when dealt make other rooms visible
        unlocks_room_id = RoomFactory.UNLOCKS_ROOM.get(room_id, Map.EMPTY)
        if unlocks_room_id != Map.EMPTY:
            RoomFactory.set_room_property(unlocks_room_id, RoomFactory.ROOM_VISIBLE_PROPERTY, True)
            room = RoomFactory.get_room_info(unlocks_room_id)
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_UNLOCK_ROOM,
                                        description=f"You explored {room_trigger.name} which makes {room.name} available"))

    def deal_and_move(self, room_id, direction):

        cx, cy = self.map.current_xy
        x, y = self.map.add_xy(cx, cy, direction)
        self.map.set_room_at(x, y, room_id)
        self.map.move(direction)

        self.post_deal_processing()

    def move(self, direction):
        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that at this time", f"{self.name} game in state {self.state}")

        self.map.move(direction)

    def end(self):
        self.state = RDGame.STATE_GAME_OVER
