# Rogue Dungeon
A random dungeon card game loosely based on Blue Prince.

## CLI interface
* `start` - start a game
* `deal` - deal some dungeon cards to explore new rooms
* `look` - show the details of your current location 
* `N` `S` `E` `W` - move around the dungeon
* `map` - display a simple dungeon map
* `quit` - end the game

## Code
The program consists of teh following packages:-
* `model` - the game and game rules
* `view` - displays formatted text views of the game (model) 
* `controller` - runs the CLI interface

### Model
`model\data\Rooms.csv` contains the room templates data that drive the game.