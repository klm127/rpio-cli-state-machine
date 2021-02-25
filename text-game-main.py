from src.Game import GameStart, GameProgram, Display
#  from src.Gpio.HitachiDisplay import HitachiPrinter

display = Display.Display()
#  display.printer = HitachiPrinter()
program = GameProgram.GameProgram(display)
program.load_state(GameStart.GameStart(program, display))