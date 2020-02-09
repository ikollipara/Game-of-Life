# src/main.py
# Ian Kollipara
# 2020.02.09
# Main Runtime for John Conway's Game of Life
#
# Usuage
# py game_of_life/src/main.py

# Imports
from simulation import Simulation

def main():
    """ Run John Conway's Game of Life Program. """
    Simulation().exec()

main()