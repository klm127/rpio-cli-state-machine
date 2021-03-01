from src.Game import GameStart, GameProgram, Display
# uncomment next line to use a Hitachi display
# from src.Gpio.HitachiDisplay import HitachiPrinter

display = Display.Display()
# uncomment next line to use a Hitachi display
# display.printer = HitachiPrinter()
program = GameProgram.GameProgram(display)
program.load_state(GameStart.GameStart(program, display))
