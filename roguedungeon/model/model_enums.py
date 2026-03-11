from enum import Enum

class RoomType(Enum):
    SHOP = 1
    PASSAGEWAY = 2
    EXIT = 3

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

def enum_value_to_key(enum_class: Enum, value: str, default=None):
    result = default
    try:
        result = enum_class._value2member_map_[value]
    except:
        pass
    return result
