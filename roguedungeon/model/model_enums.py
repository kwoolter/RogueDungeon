from enum import Enum

class RoomType(Enum):
    """ Enum for types of Room in the game """
    GAME = 'Game'
    PASSAGEWAY = 'Passageway'
    SHOP = 'Shop'
    ROOM = 'Room'
    EVIL = 'Evil'
    GOOD = 'Good'

class Rarity(Enum):
    """ Enum for Room rarity in the deck of Room cards """
    COMMONPLACE = "Commonplace"
    STANDARD = "Standard"
    UNUSUAL = "Unusual"
    RARE = "Rare"

class Direction(Enum):
    """ Enum for the directions that you can move in on the Map """
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

    def __str__(self):
        return self.value


# What is the opposite direction to each Direction
DIRECTION_REVERSE = {Direction.NORTH: Direction.SOUTH,
                     Direction.SOUTH: Direction.NORTH,
                     Direction.EAST: Direction.WEST,
                     Direction.WEST: Direction.EAST}

class Resource(Enum):
    """ Enum class for types of stackable resources in the game """
    GOLD = "Gold"
    KEYS = "Keys"
    FOOD = "Food"
    GEMS = "Gems"
    STEPS = "Steps"

    def __str__(self):
        return self.value

class Item(Enum):
    """ Enum for Items that can appear in Rooms in the game """

    CHEST_LOCKED = "a locked treasure chest"
    CHEST_UNLOCKED = "an unlocked treasure chest"
    SOFT_EARTH = "a patch of soft earth"
    EMPTY_HOLE = "an empty hole in the ground"
    ROCK_OUTCROP = "an outcrop of rock"
    RUBBISH = "a pile of rubbish"
    BOOK = "a dusty old book"
    WOOD = "some dry wood"
    FIRE = "a warm fire"
    SWORD = "a bronze sword"
    SHOVEL = "a shovel"
    PICKAXE = "a pick axe"
    TORCH = "a burning torch"
    STONE_TABLET = "a carved stone tablet"
    MAGICAL_STONE = "a magical stone"
    BED = "a simple bed"
    THIEF = "a thieving Gnome"
    THIEF_DEAD = "a dead Gnome"
    GREEN_CRYSTAL = "a green crystal ball"
    RED_CRYSTAL = "a red crystal ball"
    GREEN_CRYSTAL_PEDESTAL = "a green crystal pedestal"
    RED_CRYSTAL_PEDESTAL = "a red crystal pedestal"


    def __str__(self):
        return self.value

# Hard code where specific items need to be placed
ITEM_TO_ROOM_ID = {
    Item.GREEN_CRYSTAL_PEDESTAL: 62,
    Item.RED_CRYSTAL_PEDESTAL: 63,
    Item.BOOK: 20,
    Item.TORCH: 1
}

# What items can you interact with and...
# - What item do you need to hold to do so
# - What is the verb that you interact with
# - What item replaces the item that you interacted with
# - What rewards do you get for completing the interaction
ITEM_TO_REWARDS = {
    Item.CHEST_LOCKED : (Resource.KEYS, "unlock", Item.CHEST_UNLOCKED, (Resource.GOLD, Resource.GEMS, Resource.KEYS)),
    Item.SOFT_EARTH : (Item.SHOVEL, "dig", Item.EMPTY_HOLE, (Resource.GOLD, Resource.FOOD)),
    Item.ROCK_OUTCROP : (Item.PICKAXE, "mine", None, (Resource.GOLD, Resource.GEMS)),
    Item.WOOD : (Item.TORCH, "light", Item.FIRE, ()),
    Item.STONE_TABLET : (Item.BOOK, "translate", Item.MAGICAL_STONE, ()),
    Item.THIEF : (Item.SWORD, "kill", Item.THIEF_DEAD, (Resource.GOLD, Resource.GEMS)),
    }

# If an item is in a room what effect does it have
ITEM_TO_EFFECT = {
    Item.MAGICAL_STONE: (Resource.STEPS, 2),
    Item.FIRE : (Resource.STEPS, 2),
    Item.BED : (Resource.STEPS, 2),
    Item.THIEF : (Resource.GOLD, -2)
}

# Which items can you pick up
COLLECTABLE_ITEMS = {Item.SHOVEL, Item.TORCH, Item.PICKAXE, Item.BOOK, Item.SWORD,
                     Item.GREEN_CRYSTAL, Item.RED_CRYSTAL}

