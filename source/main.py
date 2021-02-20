"""
main

program entry point. Initializes Program (which starts with initial state)
Then sends execute command to start the desired state
"""

from Program import *

program = Program()

program.execute('gpio-001')