import re
import random

class DnD_Dice:

    def __init__(self, dnd_dice_text:str):
        self.dice_text = dnd_dice_text
        self.num_dice = 0
        self.num_dice_sides = 0
        self.bonus = 0

        self.parse_dice_text(self.dice_text)

    def __str__(self):
        return self.dice_text

    @staticmethod
    def roll_dice_from_text(dice_text)->int:

        return DnD_Dice(dice_text).roll()


    def parse_dice_text(self, dice_text):

        # Define regex for parsing the text
        number_of_dice = re.compile(r'^\d+(?=d)')
        dice_sides = re.compile(r'(?<=\dd)\d+')
        extra_bonus = re.compile(r'(?<=\d\+)\d+$')

        # Use regex to extract the dice info from the text
        r = number_of_dice.search(dice_text)
        assert r is not None, "Can't find number of dice"
        self.num_dice = int(r[0])
        r = dice_sides.search(dice_text)
        assert r is not None, "Can't find number of dice sides"
        self.num_dice_sides = int(r[0])

        # Bonus is optional
        r = extra_bonus.search(dice_text)
        if r is not None:
            self.bonus = int(r[0])
        else:
            self.bonus = 0


    def roll(self):

        # Now time to roll the dice!
        result = 0

        for i in range(self.num_dice):
            result += random.randint(1, self.num_dice_sides)

        result += self.bonus

        return result

    from functools import lru_cache

    @lru_cache(None)
    @staticmethod
    def ways(num_dice : int, dice_sides : int, dice_sum : int):
        if num_dice == 1:
            return 1 if 1 <= dice_sum <= dice_sides else 0

        return sum(DnD_Dice.ways(num_dice - 1, dice_sides, dice_sum - i) for i in range(1, dice_sides + 1))

    @staticmethod
    def probability(num_dice : int, dice_sides : int, dice_sum : int):
        return DnD_Dice.ways(num_dice, dice_sides, dice_sum) / (dice_sides ** num_dice)



def run_tests():

    dice_rolls = ["1d6", "1d4+1", "1d20"]

    for dice in dice_rolls:

        d1 = DnD_Dice(dice)
        r = d1.roll()
        print(f'Rolling {d1} dice....result = {r}')


    for dice in dice_rolls:
        r=DnD_Dice.roll_dice_from_text(dice)
        print(f'Rolling {dice} dice....result = {r}')

    num_dice = 3
    dice_sides = 20
    for i in range(num_dice,num_dice * dice_sides + 1):
        print(f'{i}, {DnD_Dice.probability(num_dice, dice_sides, i):.3f}')



if __name__ == "__main__":
    run_tests()



