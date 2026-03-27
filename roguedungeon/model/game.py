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
        return self.events.popleft()

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

    # How much of each resource do you start the game with
    RESOURCE_ALLOWANCE = {
        Resource.GOLD: 20,
        Resource.STEPS: 30,
        Resource.GEMS: 1,
        Resource.KEYS: 1
    }

    # What is the price of each resource
    RESOURCE_PRICES = {
        Resource.GOLD: 1,
        Resource.FOOD: 5,
        Resource.GEMS: 5,
        Resource.KEYS: 5
    }

    def __init__(self, name: str):
        self.name = name
        self.map = None
        self.state = RDGame.STATE_LOADED
        self.resources = {}
        self.events = EventQueue()
        self.deck = None

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

        # Add some items to the map
        item = Item.CHEST_LOCKED
        for i in range(10):
            self.map.add_item_at(random.randint(0, self.map.max_width - 1),
                                 random.randint(0, self.map.max_height - 1),
                                 item)

        # Allocate the daily resource allowances
        for resource in Resource:
            quantity = RDGame.RESOURCE_ALLOWANCE.get(resource, 0)
            self.resources[resource] = quantity

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

    def take_resource(self, resource: Resource, pay: bool = False):
        """Take all the specified resource at the current room and add it to your inventory"""

        # Get the current square and see how much of the specified resource there is
        square = self.get_current_map_square()
        resource_quantity = square.get_resource(resource)

        # If there are some of the specified resources here...
        if resource_quantity > 0:

            # Check if we are trying to take items from a Shop
            if square.room.room_type == RoomType.SHOP.value:

                # Find out the price of the resource
                price = RDGame.RESOURCE_PRICES.get(resource, 0)

                # See if we have enough money
                if price > self.resources[Resource.GOLD]:
                    self.events.add_event(Event(type=Event.GAME_ACTION_FAILED,
                                                name=Event.GAME_TAKE_RESOURCE,
                                                description=f"You don't have enough gold to buy {resource} for {price} gold each"))

                    raise ApplicationException("Take Resource Failed",
                                               f"You don't have enough gold to buy {resource} for {price} gold each")

                # If we do that decrement our gold and set resource quantity to 1 - you can only buy 1 item at a time
                else:
                    self.resources[Resource.GOLD] -= price
                    resource_quantity = 1

                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.GAME_BUY_RESOURCE,
                                                description=f"You pay {price} gold for {resource_quantity} {resource} at the shop"))

            # Add the resources to your inventory
            self.resources[resource] += resource_quantity

            # Change the available resources in the square
            square.add_resource(resource, -resource_quantity)
            if square.resources[resource] == 0:
                del square.resources[resource]

            # Print what just happened
            s = ""
            if resource_quantity > 1:
                s = "s"
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_TAKE_RESOURCE,
                                        description=f"You take {resource_quantity} {resource} from {square.room.name}"))

        # Else you are trying to take a resource that is not here
        else:
            raise ApplicationException("Take Resource", f"There is no {resource.value} here")

        # Eat any food that you have and convert if to steps
        if self.resources[Resource.FOOD] > 0:
            self.resources[Resource.STEPS] += self.resources[Resource.FOOD]
            self.resources[Resource.FOOD] = 0
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_EAT_FOOD,
                                        description=f"You eat {resource_quantity} food and now have {self.resources[Resource.STEPS]} steps"))

    def get_adjacent_blank_squares(self):
        """
        :return: Get the list of adjacent squares that are empty
        """

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
        """
        Deal a list of rooms that match some search criteria

        :param direction: which direction are we trying to head in
        :return: a list of rooms that match the search criteria
        """

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
        self.pre_deal_processing(direction)

        # Try 3 times to get at least 3 cards
        for i in range(3):

            # Deal some cards
            results = self.deck.get_matching_rooms()

            # We got at least 3 cards so all good
            if len(results) >= 3:
                break
            # Else tweak the query parameters to try and get more matching rooms
            else:
                print(f"\tDEBUG:On deal {i + 1} we only got {len(results)} matching cards so trying again...")
                max_rarity_int = min(RoomFactory.RARITY_TO_INT[self.deck.max_rarity] + 1,
                                     max(RoomFactory.RARITY_TO_INT.values()))
                self.deck.max_rarity = RoomFactory.INT_TO_RARITY[max_rarity_int]
                self.deck.max_exits += 1

        # If we still only got 3 or less results so just use these
        if len(results) <= 3:
            print(f"\tDEBUG:Deal only got {len(results)} matching cards")
            rooms = results
        # Else sample 3 random cards
        else:
            rooms = random.sample(results, k=3)

        return rooms

    def pre_deal_processing(self, direction):
        """Put any logic here that you want to kick-in before the deal is made"""
        pass

    def is_exit_locked(self, direction: Direction):
        # Get details of the current room
        current_square = self.map.get_map_square_at()
        return current_square.is_exit_locked(direction)

    def lock_random_exits(self):
        """ Lock some random exits in the current room based on some random logic"""

        # Get details of the current room
        current_square = self.map.get_map_square_at()

        # Run a random check to see if we want to add a lock based on current y
        rank = current_square.y
        # rank = 999 # debug
        if random.randint(0, self.map.max_height) < rank:

            # Find which exits have not yet been explored
            exits = self.get_adjacent_blank_squares()

            # If we find some then randomly pick some exits and lock them
            if len(exits) > 0:

                # How many exits are we locking?
                k = min(random.randint(0, (rank + 1) // 3), len(exits))

                # Get a random sample of k exits and lock each one
                for exit_to_lock in random.sample(exits, k=k):
                    current_square.lock_exit(exit_to_lock)
                    self.events.add_event(Event(type=Event.DEBUG,
                                                name=Event.GAME_LOCK_EXIT,
                                                description=f"Locked {exit_to_lock.value} exit in {current_square.room.name}"))
        else:
            self.events.add_event(Event(type=Event.DEBUG,
                                        name=Event.GAME_LOCK_EXIT,
                                        description=f"No exits were locked in {current_square.room.name}"))

    def get_locked_exits(self):
        # Get details of the current room
        current_square = self.map.get_map_square_at()

        return list(current_square.locks)

    def unlock_exit(self, direction: Direction):
        """
        Attempt to unlock the exit in the specified direction
        :param direction: which exit is to be unlocked?
        :return:
        """

        # Get details of the current room
        current_square = self.map.get_map_square_at()

        # If the exit is locked
        if current_square.is_exit_locked(direction):

            # ...and you have a key
            if self.resources.get(Resource.KEYS, 0) > 0:

                # Unlock the specified exit
                current_square.lock_exit(direction, False)
                self.resources[Resource.KEYS] -= 1
                # print(f"\tYou used a key to unlock the {direction.value} from {current_square.room.name}")

            else:
                raise ApplicationException("Unlock Exit",
                                           f"You don't have any keys to unlock the {direction} exit from {current_square.room.name}")
        else:
            raise ApplicationException("Unlock Exit", f"Exit {direction} from {current_square.room.name} is not locked")

    def unlock_chest(self):
        """ Attempt to unlock a chest at the current location """

        # Get the details of the current square
        square = self.get_current_map_square()

        # Is there a locked chest here?
        if square.get_item(Item.CHEST_LOCKED) > 0:

            # See if you have a key to use to unlock...
            if self.resources.get(Resource.KEYS, 0) > 0:
                square.set_item(Item.CHEST_LOCKED, 0)
                square.add_item(Item.CHEST_UNLOCKED, 1)
                self.events.add_event(Event(type=Event.GAME,
                                            name=Event.GAME_ACTION_SUCCEEDED,
                                            description=f"You use a key to open {Item.CHEST_LOCKED.value}"))

                # Allocate some random rewards
                rewards = {Resource.GOLD: random.randint(0, 3),
                           Resource.GEMS: random.randint(0, 3),
                           Resource.KEYS: random.randint(0, 3)}

                for k, v in rewards.items():
                    square.add_resource(k, v)
                    if v > 0:
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.GAME_ACTION_SUCCEEDED,
                                                    description=f"You find {k.value} x {v} in the chest"))

            else:
                self.events.add_event(Event(type=Event.GAME,
                                            name=Event.GAME_ACTION_FAILED,
                                            description=f"You don't have a key to open {Item.CHEST_LOCKED.value}"))
        else:
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_ACTION_FAILED,
                                        description=f"Nothing to open here"))

    def post_deal_processing(self):
        """Put any logic here that you want to kick-in once a new room card has been selected """

        # Get details of the current room square
        room_id = self.map.current_room_id
        current_square = self.map.get_map_square_at()
        current_room = current_square.room

        # Deduct the gem cost of the room that you chose to deal
        if current_room.cost > 0:
            s = ""
            if current_room.cost > 1:
                s = "s"
            self.resources[Resource.GEMS] -= current_room.cost
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_SPEND_GEMS,
                                        description=f"You spent {current_room.cost} gem{s} on exploring {current_room.name}"))

        # Add the number of bonus steps gained from dealing the room
        bonus_steps = current_square.get_resource(Resource.STEPS)
        if bonus_steps != 0:
            s = ""
            if abs(bonus_steps) > 1:
                s = "s"

            # Increment our steps by the bonus
            self.resources[Resource.STEPS] += bonus_steps

            # Set the square's bonus steps to 0
            current_square.set_resource(Resource.STEPS, 0)

            # Trigger an event if you gain or lose steps
            # Gain steps
            if bonus_steps > 0:
                self.events.add_event(Event(type=Event.GAME,
                                            name=Event.GAME_STEP_BONUS,
                                            description=f"You gain {bonus_steps} step{s} from exploring {current_room.name}."))
            # Lose steps
            else:
                self.events.add_event(Event(type=Event.GAME,
                                            name=Event.GAME_STEP_PENALTY,
                                            description=f"You lose {abs(bonus_steps)} step{s} from exploring {current_room.name}."))

        # Decrement the number of steps that you have left
        self.resources[Resource.STEPS] -= 1
        self.events.add_event(Event(type=Event.DEBUG,
                                    name=Event.GAME_TAKE_STEP,
                                    description=f"You have {self.resources[Resource.STEPS]} steps left."))

        # If you have run out of steps then it is game over!
        if self.resources[Resource.STEPS] <= 0:
            self.state = RDGame.STATE_GAME_OVER
            self.events.add_event(Event(type=Event.STATE,
                                        name=Event.STATE_GAME_OVER,
                                        description=f"You ran out of steps. You failed to complete the Rogue Dungeon."))

        # Run some logic to randomly lock some of the new square's exits
        self.lock_random_exits()

        # If we have got to the end of the dungeon then set the game state to victory
        if room_id == Map.EXIT_END:
            self.state = RDGame.STATE_VICTORY
            self.events.add_event(Event(type=Event.STATE,
                                        name=Event.STATE_VICTORY,
                                        description=f"Victory! You have completed the Rogue Dungeon in {self.moves} moves."))

        # Process rooms that when dealt make other rooms visible
        unlocks_room_id = RoomFactory.UNLOCKS_ROOM.get(room_id, Map.EMPTY)
        if unlocks_room_id != Map.EMPTY:
            RoomFactory.set_room_property(unlocks_room_id, RoomFactory.ROOM_VISIBLE_PROPERTY, True)
            room = RoomFactory.get_room_info(unlocks_room_id)
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_UNLOCK_ROOM,
                                        description=f"You explored {current_room.name} which makes {room.name} available"))

    def deal_and_move(self, room_id, direction):

        # Check that the exit from this square in the specified direction is not locked.
        square = self.get_current_map_square()
        if square.is_exit_locked(direction):
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_ACTION_FAILED,
                                        description=f"Exit {direction} from {square.room.name} is locked."))

            raise ApplicationException("Exit is locked", f"Exit {direction} from {square.room.name} is locked.")

        # Check that you can afford the new room
        room = RoomFactory.get_room_info(room_id)
        if room.cost > self.resources[Resource.GEMS]:
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_ACTION_FAILED,
                                        description=f"You don't have enough gems to buy {room.name} (cost = {room.cost})"))

            raise ApplicationException("Room Cost",
                                       f"You don't have enough gems to buy {room.name} (cost = {room.cost})")

        # find the x,y for the new room based on the current x,y and the direction vector
        cx, cy = self.map.current_xy
        x, y = self.map.add_xy(cx, cy, direction)

        # Place the new room at the x,y
        self.map.set_room_at(x, y, room_id)

        # Move the player to the new room
        self.map.move(direction)

        # Run any logic that needs to be done after a new room has been dealt
        self.post_deal_processing()

    def move(self, direction):
        if self.state != RDGame.STATE_PLAYING:
            raise ApplicationException("Cannot do that at this time", f"{self.name} game in state {self.state}")

        # Attempt to move the player in the specified direction
        self.map.move(direction)

        # Decrement the number of steps that you have left
        self.resources[Resource.STEPS] -= 1
        self.events.add_event(Event(type=Event.DEBUG,
                                    name=Event.GAME_TAKE_STEP,
                                    description=f"You have {self.resources[Resource.STEPS]} steps left."))

        # If you have run out of steps then it is game over!
        if self.resources[Resource.STEPS] <= 0:
            self.state = RDGame.STATE_GAME_OVER
            self.events.add_event(Event(type=Event.STATE,
                                        name=Event.STATE_GAME_OVER,
                                        description=f"You ran out of steps. You failed to complete the Rogue Dungeon."))

        # If we have got to the end of the dungeon then set the game state to victory
        if self.map.current_room_id == Map.EXIT_END:
            self.state = RDGame.STATE_VICTORY
            self.events.add_event(Event(type=Event.STATE,
                                        name=Event.STATE_VICTORY,
                                        description=f"Victory! You have completed the Rogue Dungeon in {self.moves} moves."))

    def end(self):
        self.state = RDGame.STATE_GAME_OVER
