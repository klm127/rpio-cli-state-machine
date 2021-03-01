Game
----
The Game module consists of classes needed to play a text-based ASCII game on 2 16 character lines, such as could be printed to console or shown on a Hitachi display.

Classes in Game module extend those of StateMachine and utilize the same Program -> State -> Command structure.

Commands are sent to the `GameState` after using pynput to parse key presses.

The initial game state, in `GameStart`, creates a few text scroll and animated "spinner" objects from `TitleScreenObjects` to describe the game, then loads `MapState`, which utilizes the `Map` library to provide the structure of the game world.