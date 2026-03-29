from enum import Enum

class RoomType(Enum):
    GAME = 'Game'
    PASSAGEWAY = 'Passageway'
    SHOP = 'Shop'
    ROOM = 'Room'
    EVIL = 'Evil'
    GOOD = 'Good'

class Rarity(Enum):
    COMMONPLACE = "Commonplace"
    STANDARD = "Standard"
    UNUSUAL = "Unusual"
    RARE = "Rare"

class Direction(Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

    def __str__(self):
        return self.value


DIRECTION_REVERSE = {Direction.NORTH: Direction.SOUTH,
                     Direction.SOUTH: Direction.NORTH,
                     Direction.EAST: Direction.WEST,
                     Direction.WEST: Direction.EAST}

class Resource(Enum):
    GOLD = "Gold"
    KEYS = "Keys"
    FOOD = "Food"
    GEMS = "Gems"
    STEPS = "Steps"

    def __str__(self):
        return self.value

class Item(Enum):

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

    def __str__(self):
        return self.value


ITEM_TO_REWARDS = {
    Item.CHEST_LOCKED : (Resource.KEYS, "unlock", Item.CHEST_UNLOCKED, (Resource.GOLD, Resource.GEMS, Resource.KEYS)),
    Item.SOFT_EARTH : (Item.SHOVEL, "dig", Item.EMPTY_HOLE, (Resource.GOLD, Resource.FOOD)),
    Item.ROCK_OUTCROP : (Item.PICKAXE, "mine", None, (Resource.GOLD, Resource.GEMS)),
    Item.WOOD : (Item.TORCH, "light", Item.FIRE, ()),
    Item.STONE_TABLET : (Item.BOOK, "translate", Item.MAGICAL_STONE, ()),
    Item.THIEF : (Item.SWORD, "kill", Item.THIEF_DEAD, (Resource.GOLD, Resource.GEMS)),
    }

ITEM_TO_EFFECT = {
    Item.MAGICAL_STONE: (Resource.STEPS, 2),
    Item.FIRE : (Resource.STEPS, 2),
    Item.BED : (Resource.STEPS, 3),
    Item.THIEF : (Resource.GOLD, -2)
}

COLLECTABLE_ITEMS = {Item.SHOVEL, Item.TORCH, Item.PICKAXE, Item.BOOK, Item.SWORD}

def enum_value_to_key(enum_class: Enum, value: str, default=None):
    result = default
    try:
        result = enum_class._value2member_map_[value]
    except:
        pass
    return result
