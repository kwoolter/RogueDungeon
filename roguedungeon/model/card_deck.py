from roguedungeon.model.rooms import *
import random

class RoomCardDeck:

    def __init__(self):
        self.cards = []
        self.current_x = 0
        self.current_y = 0
        self.mandatory_exit = Direction.NORTH
        self.min_exits = 1
        self.max_exits = 4
        self.min_rank = 1
        self.max_rank = 9
        self.min_rarity = "Commonplace"
        self.max_rarity = "Rare"
        self.visible = True

    def initialise(self):
        RoomFactory.load("rooms.csv")

    def deal(self, mandatory_exit):

        rooms = []

        results = self.get_matching_rooms()

        return results

    def get_matching_rooms(self):

        results = RoomFactory.get_matching_rooms(self.mandatory_exit,
                                                 self.min_exits,
                                                 self.min_rank, self.max_rank,
                                                 self.min_rarity, self.max_rarity,
                                                 self.visible)

        return results


def test():

    deck = RoomCardDeck()
    deck.initialise()

    results = deck.get_matching_rooms()
    for room in results:
        print(room)



if __name__ == "__main__":
    test()