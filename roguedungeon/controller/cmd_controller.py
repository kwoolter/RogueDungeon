import cmd
import roguedungeon.model as model
import roguedungeon.view as view
import logging

from roguedungeon.model import Event, ApplicationException


class RDCLI(cmd.Cmd):
    intro = "Welcome to the Rogue Dungeon CLI.\n" \
            "Type 'start' to get playing the game.\n" \
            "Type 'help' to see available commands.\n"
    prompt = "What next?"

    def __init__(self):
        super().__init__(completekey='tab')
        self.game = None
        self.game_view = None

        # Used to control if DEBUG Events are displayed
        self._DEBUG = False

    def do_start(self, arg):
        """Start the game"""

        # Create and initialise the game
        self.game = model.RDGame("Rogue Dungeon")
        self.game.initialise()

        # Initialise the game view and print
        view.TextView.initialise()
        self.game_view = view.GameTextView(self.game)
        self.game_view.print()
        self.print()

        # Process any events that got raised
        self.process_events()

    def do_quit(self, arg):
        """Finish the current game"""

        # Check if the player wants to quit
        if confirm("Are you sure you want to quit?") == True:

            # Run the game end
            self.game.end()

            # Print the game status
            self.game_view.print()

            # Print the final map
            v = view.MapTextView(self.game.map)
            v.print2()

            # Process any events that got raised
            self.process_events()

            # return True to exit Cmd the loop
            return True

        else:
            print("Let's keep going...")
            return False

    def run(self):
        """Run the CLI loop"""
        self.cmdloop()

    def process_events(self):
        # Loop to process game events
        event = self.game.get_next_event()

        while event is not None:

            # Print the event
            if event.type != Event.DEBUG or self._DEBUG is True:
                v = view.EventTextView(event)
                v.print()

            event = self.game.get_next_event()

        # Check if the game is over
        if self.game.state in (model.RDGame.STATE_VICTORY, model.RDGame.STATE_GAME_OVER):
            self.game_over()

    def do_status(self, arg):
        """Print the status of game"""
        try:

            if self.game is not None:
                v = view.GameTextView(self.game)
                v.print()

                # Process any events that got raised
                self.process_events()

        except BaseException as e:
            print(e)
            # Process any events that got raised
            self.process_events()

    def do_map(self, arg):
        """Print the game map"""

        try:

            # Set up a view of the game map and print it
            v = view.MapTextView(self.game.map)
            # v.print()
            v.print2()
            print(f"\nRooms = {self.game.map.rooms}, Moves = {self.game.map.moves}")

            # Process any events that got raised
            self.process_events()

        except BaseException as e:
            print(e)
            # Process any events that got raised
            self.process_events()

    def do_look(self, arg):
        """Take a look around the current room"""
        self.print()

    def do_n(self, args):
        """Move North"""
        return self.do_N(args)

    def do_N(self, args):
        """Move North"""
        self.move(model.Direction.NORTH)

    def do_s(self, args):
        """Move South"""
        return self.do_S(args)

    def do_S(self, args):
        """Move South"""
        self.move(model.Direction.SOUTH)


    def do_e(self, args):
        """Move East"""
        return self.do_E(args)

    def do_E(self, args):
        """Move East"""
        self.move(model.Direction.EAST)


    def do_w(self, args):
        """Move West"""
        return self.do_W(args)

    def do_W(self, args):
        """Move West"""
        self.move(model.Direction.WEST)


    def do_use(self, args):
        """ Try interacting with something that you can see at the current location"""

        try:
            items = self.game.get_square_items()
            item = pick("Item", items, auto_pick=True)
            if item is not None:
                self.game.use_item(item)
                # Process any events that got raised
                self.process_events()

        except BaseException as e:
            print(e)
            # Process any events that got raised
            self.process_events()

    def do_unlock(self, args):
        """Use keys to unlock exits"""
        try:

            # Get a list of exits that are locked
            choices = self.game.get_locked_exits()

            # If there are locked exits...
            if len(choices) > 0:

                # See if you have a key to use to unlock...
                if self.game.resources.get(model.Resource.KEYS, 0) > 0:

                    # Pick the exit that you want to unlock
                    direction = pick("Exit", choices, auto_pick=True)

                    # Unlock the selected exit
                    if direction is not None:
                        self.game.unlock_exit(direction)
                        print(f"You used a key to unlock the {direction} exit")

                # You don't have a key
                else:
                    print("You don't have any keys!")

            # No locked exits
            else:
                print("There are no locked exits here")

        except BaseException as e:
            print(e)
            # Process any events that got raised
            self.process_events()

    def do_deal(self, arg):
        """Deal a room to explore a new square on the Map"""

        try:

            # Get the list of exits in the room that have yet to be explored
            exits = self.game.get_adjacent_blank_squares()

            # Get the player to pick the direction that they wish to explore
            direction = pick("Direction", exits)

            # If they picked a direction...
            if direction is not None:

                # Check if the chosen direction is unlocked
                if self.game.is_exit_locked(direction):
                    print(f"Exit {direction} is locked.")

                else:

                    print(f"Exploring {direction}...")

                    # Deal some cards that have an exit in the opposite direction
                    opp_exit = model.DIRECTION_REVERSE[direction]
                    rooms = self.game.deal(opp_exit)

                    # Pick a room card - no cancels allowed, they have to pick a card
                    room = pick("Room", rooms, cancel=False)

                    # Deal the selected card and move to the new location
                    print(f"Exploring {room}")
                    self.game.deal_and_move(room.room_id, direction)

                    # Print the new location
                    self.print()

                    # Process any events that got raised
                    self.process_events()

        except BaseException as e:
            print(e)
            # Process any events that got raised
            self.process_events()

    def do_get(self, args):
        """ Get a resource from the current room"""
        try:
            # See what resources are available at the current square
            resources = self.game.get_square_resources()
            items = model.COLLECTABLE_ITEMS.intersection(self.game.get_square_items())
            resources.extend(list(items))

            # Pick the resource that you want to get
            resource = pick("Item", resources, auto_pick=True)

            # If a valid selection was made...
            if resource is not None:

                if type(resource) == model.Resource:
                    # Take the selected resource
                    self.game.take_resource(resource)
                elif type(resource) == model.Item:
                    # Take the selected item
                    self.game.take_item(resource)
                else:
                    print(f"Can't take {resource} of type {type(resource)}")

            # Process any events that got raised
            self.process_events()

        except ApplicationException as e:
            # Process any events that got raised
            self.process_events()

        except Exception as e:
            print(e)
            self.process_events()

    def move(self, direction):
        try:
            # Move in the specified direction and print the new location
            self.game.move(direction)
            self.print()

        except ApplicationException as e:
            # Process any events that got raised
            self.process_events()

        except Exception as e:
            print(e)
            self.process_events()




    def game_over(self):
        """ Game Over routine"""

        # Check if you successfully completed the game
        if self.game.state == model.RDGame.STATE_VICTORY:
            print(f"Congratulations - you completed {self.game.name}")

        # Print the game status
        v = view.GameTextView(self.game)
        v.print()

    def print(self):
        try:
            square = self.game.get_current_map_square()
            v = view.MapSquareTextView(square)
            v.print()
        except BaseException as e:
            print(f"Error {e}")


# Function to ask the user a simple Yes/No confirmation and return a boolean
def confirm(question: str):
    choices = ["Yes", "No"]

    while True:
        print(question)
        for i in range(0, len(choices)):
            print("%i. %s" % (i + 1, choices[i]))
        choice = input("Choice?")
        if choice.isdigit() and int(choice) > 0 and int(choice) <= (len(choices)):
            break
        else:
            print("Invalid choice.  Try again!")

    return int(choice) == 1


# Function to present a menu to pick an object from a list of objects
# auto_pick means if the list has only one item then automatically pick that item
def pick(object_type: str, objects: list, cancel=True, auto_pick: bool = False):
    selected_object = None
    choices = len(objects)
    vowels = "AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good then raise an exception
    if objects is None or choices == 0:
        raise (Exception("No %s to pick from." % object_type))

    # If you selected auto pick and there is only one object in the list then pick it
    if auto_pick is True and choices == 1:
        selected_object = objects[0]

    # While an object has not yet been picked...
    while selected_object == None:

        # Print the menu of available objects to select
        print("Select %s %s:-" % (a_or_an, object_type))

        for i in range(0, choices):
            print("\t%i) %s" % (i + 1, str(objects[i])))

        # Along with an extra option to cancel selection
        if cancel is True:
            print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if choice.isdigit() is True:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice - 1]
                logging.info("pick(): You chose %s %s." % (object_type, str(selected_object)))
            elif choice == (choices + 1) and cancel is True:
                break
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object
