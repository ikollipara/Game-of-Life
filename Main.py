from Simuation import Simulation
from getFunctions import *

def main():
    sim = Simulation()
    sim.intro()
    sim.help()
    sim.add_world(60, 20)
    sim.world.populate()
    sim.world.find_neighbors()
    print(sim.world)
    repeat = True
    while repeat:
        command, parameter = sim.menu()
        sim.run(command, parameter)
        if command == 'e':
            repeat = False
    sim.outro()
main()
