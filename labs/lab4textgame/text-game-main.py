from src.StateMachine import *
from src.Game import *

import time
from pynput import keyboard

program = Program.Program()
print(program)
program.load_state(GameStart.GameStart(program))
