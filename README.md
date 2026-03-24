# Rogue Dungeon
A random dungeon card game loosely based on Blue Prince.

## CLI interface
* `start` - start a game
* `deal` - deal some dungeon cards to explore new rooms
* `look` - show the details of your current location 
* `N` `S` `E` `W` - move around the dungeon
* `get` - get a resource from the current location
* `map` - display a simple dungeon map
* `status` - diaplay the game status
* `quit` - end the game

## Code
The program consists of the following packages:-
* `roguedungeon` - the main package with the following sub-packages
* `model` - the game and game rules
* `view` - displays formatted text views of the game (model) 
* `controller` - runs the CLI interface

### Model
`model\data\Rooms.csv` [file](https://raw.githubusercontent.com/kwoolter/RogueDungeon/refs/heads/master/roguedungeon/model/data/Rooms.csv) contains the room templates data that drive the game.

## Screenshots
<table>
<tr>
<td>
<img height=233 width=484 src="https://github.com/kwoolter/RogueDungeon/blob/master/screenshots/Capture1.PNG" alt="game1">
</td>
<td>
<img height=677 width=305 src="https://github.com/kwoolter/RogueDungeon/blob/master/screenshots/Capture2.PNG" alt="game2">
</td>
</tr>
</table>
