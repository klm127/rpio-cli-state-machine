from src.Game import GameStart, GameProgram, Display

display = Display.Display()
program = GameProgram.GameProgram(display)
program.load_state(GameStart.GameStart(program, display))