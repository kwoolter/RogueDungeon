
class Event():

    # Event Types
    DEBUG = "Debug"
    QUIT = "Quit"
    DEFAULT = "default"
    STATE = "State"
    GAME = "Game"
    CONTROL = "control"
    EFFECT = "effect"
    GAME_ACTION_SUCCEEDED = "Action Succeeded"
    GAME_ACTION_FAILED = "Action Failed"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"
    STATE_VICTORY = "Victory"



    # Game events
    GAME_UNLOCK_ROOM = "Unlock Room"
    GAME_LOCK_EXIT = "Lock Exit"
    GAME_TAKE_RESOURCE = "Take Resource"
    GAME_TAKE_ITEM = "Take Item"
    GAME_BUY_RESOURCE = "Buy Resource"
    GAME_USE_ITEM = "Use Item"
    GAME_SPEND_GEMS = "Spend Gems"
    GAME_EAT_FOOD = "Eat Food"
    GAME_TAKE_STEP = "Take a Step"
    GAME_STEP_BONUS = "Step Bonus"
    GAME_STEP_PENALTY = "Step Penalty"
    GAME_ITEM_BONUS = "Item Effect"
    GAME_ITEM_PENALTY = "Item Penalty"


    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)