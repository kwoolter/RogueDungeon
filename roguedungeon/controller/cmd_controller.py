import cmd
import roguedungeon.model as model
import roguedungeon.view as view
import logging


class RDCLI(cmd.Cmd):
    intro = "Welcome to the Rogue Dungeon CLI.\n" \
            "Type 'help' to see available commands.\n"
    prompt = "What next?"

    def __init__(self):
        super().__init__(completekey='tab')
        self.game = None

    def do_start(self, arg):
        'Start the game'
        self.game = model.RDGame()
        self.game.initialise()
        view.TextView.initialise()

        self.print()

    def run(self):
        self.cmdloop()

    def do_status(self, arg):
        'Print status of game'
        self.game.print()
        self.print()

    def do_N(self, args):
        'Move North'
        self.move(model.Direction.NORTH)

    def do_S(self, args):
        'Move South'
        self.move(model.Direction.SOUTH)

    def do_E(self, args):
        'Move East'
        self.move(model.Direction.EAST)

    def do_W(self, args):
        'Move West'
        self.move(model.Direction.WEST)

    def do_deal(self, arg):
        'Deal a new room to fill a square on the Map'

        try:
            exits = self.game.get_adjacent_blank_squares()
            direction = pick("Direction", list(exits))
            print(f"Opening the door {direction}...")
            opp_exit = model.DIRECTION_REVERSE[direction]
            rooms = self.game.deck.get_rooms_by_exit(opp_exit)
            room = pick("Room", rooms)
            print(f"Dealing {room}")

            self.game.deal_and_move(room.room_id, direction)
            self.print()

        except BaseException as e:
            print(e)

    def move(self, direction):
        try:
            self.game.move(direction)
            self.print()
        except BaseException as e:
            print(str(e))

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

    return (int(choice) == 1)


# Function to present a menu to pick an object from a list of objects
# auto_pick means if the list has only one item then automatically pick that item
def pick(object_type: str, objects: list, auto_pick: bool = False):
    selected_object = None
    choices = len(objects)
    vowels = "AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good the raise an exception
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
        print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if choice.isdigit() is True:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice - 1]
                logging.info("pick(): You chose %s %s." % (object_type, str(selected_object)))
            elif choice == (choices + 1):
                break
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object
