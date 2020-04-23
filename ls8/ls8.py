#!/usr/bin/env python3
"""Main."""
import sys
from cpu import *

cpu = CPU()
if len(sys.argv) > 1:
    cpu.load(sys.argv[1])
    cpu.run()
else:
    print('\nError!, no program has been specified to run. Enter the path to the file after the "py ls8.py"')
