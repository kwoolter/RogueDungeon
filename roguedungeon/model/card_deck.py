from .rooms import *

class RoomCardDeck:

    def __init__(self):
        self.cards = None

    def initialise(self):
        RoomFactory.load("rooms.csv")
        self.cards = []

    def load(self, exit, rarity = 100, rank = 100):
        pass

    def get_rooms_by_exit(self, direction):
        rooms = RoomFactory.get_rooms_by_exit(direction.value)
        return rooms


def test():

    deck = RoomCardDeck()
    deck.initialise()



if __name__ == "__main__":
    test()