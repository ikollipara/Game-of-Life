# src/simulation.py
# Ian Kollipara
# 2020.02.09
# Simulation Class for JCGoL
#
# Usage
# from simulation import Simulation

# Imports
from world import World
from utils import get_integer, get_bool
from os import listdir

class Simulation:
    """ Implement a Simulation class for use in John Conway's Game of Life.
    
    Simulation contains the main game loop, as well as the action methods.
    """

    # Instance Variables (public)
    # world               The current instance of the World class
    # simulation_actions  A dictionary containing all accessable methods for use in the Simulation
    # past_iterations     A list of past versions of the current world instance

    def __init__(self):
        """ __init__() create a Simulation Object.
        
        Usage
        s = Simulation()
        s.exec()
        """
        self.world = World()

        # Lambda functions used to keep dictionary uniform with accepting parameters
        self.simulation_actions = {
            's': self.simulate_to_x_generation,
            'k': self.skip_to_x_generation,
            'a': lambda param: self.advance_to_next_generation(),
            'c': self.create_new_world,
            'v': self.save_current_world,
            'l': self.load_world_from_save,
            'p': self.adjust_world_population_rate,
            't': self.adjust_torus,
            'h': lambda param: self.help_menu(),
            'u': lambda param: self.auto_sim(),
            'e': lambda param: None,
        }
        self.past_iterations = []
    
    def simulate_to_x_generation(self, final_generation):
        """ Display each iteration of self.world until generation x. 
        
        Parameters
        final_generation  Integer to simulate to
        """

        for _ in range(int(final_generation)):
            self.past_iterations.append(self.world.stringify())
            self.world.advance_generation()
            print(self.world)
    
    def skip_to_x_generation(self, final_generation):
        """ Display self.world at generation x. 
        
        Parameters
        final_generation  Integer to skip to
        """

        for _ in range(int(final_generation)):
            self.past_iterations.append(self.world.stringify())
            self.world.advance_generation()
        
        print(self.world)

    def advance_to_next_generation(self):
        """ Display self.world's next generation. """

        self.past_iterations.append(self.world.stringify())
        self.world.advance_generation()
        print(self.world)
    
    def create_new_world(self, size):
        """ Generate a new World Instance. 
        
        Parameters
        size  Tuple of integers used to generate world size (rows, columns)
        """

        row, columns = size.split(' ')
        self.world = World((int(row), int(columns)))
        self.past_iterations.clear()
    
    def save_current_world(self, save_name):
        """ Save the current_world to save name given. 
        
        Parameters
        save_name  String used to generate savefile
        """

        override = True

        if save_name in listdir("Saves"):
            override = get_bool("Do you want to override previous save? ")

        if not override:
            save_name = input("What is the new save name? ")

        with open(f"Saves/{save_name}", "w+") as new_world_save:
            new_world_save.write(self.world.stringify())
    
    def load_world_from_save(self, filename):
        """ Set World Instance to saved file. 
        
        Parameters
        filename  String containing the name of the file to be loaded
        """
        
        # TODO: Finish Loading Section
        try:
            if filename in listdir("Saves"):

                with open(f"Saves/{filename}") as world_save:
                    self.world = World.from_save_file(world_save)
                    self.past_iterations.clear()
            
            else:
                print(f"{filename} doesn't exist")

        except:
            print("Loading is still in production")
        
    def adjust_world_population_rate(self, population_rate):
        """ Regenerate self.world with given population_rate. 
        
        Parameters
        population_rate  Integer used to figure out the percent alive cells. (population_rate/100)
        """
        
        self.world = World(self.world.size, int(population_rate))
    
    def adjust_torus(self, option):
        """ Set self.world's torus status. """
        
        options = {
            'on': True,
            'off': False
        }

        self.world.is_torus = options[option]

    def help_menu(self, ):
        """ Display the help menu for commands. """

        print("""
        This program allows the user to simulate cellular life using John Conway's model.
        In this model every cell will die if it has under 2 or 4+ neighbors. The cell will
        stay alive if it falls outside those parameters. If the cell has exactly 3 neighbors
        it will become alive. This leads to patterns and an overall interesting experience. 
        This version was developed by Ian Kollipara
        ---------------------------------------------------------------------------------------
                Commands    |   Meaning
        Advance             | Move forward 1 generation
        Sim                 | Move forward x generations
        Skip                | Move to, without showing, x generation
        Save                | Save current world in a directory called "Saves"
        Load                | Loads the specified saved world from "Saves"
        Populate            | Repopulate the current world via a given percent
        Auto                | Automatically Simulate the world until stable
        Create              | Create a New World via size
        Help                | Brings up this menu
        Exit                | Quits the Program
        ----------------------------------------------------------------------------------------
        """)

    def auto_sim(self):
        """ Simulate automatically until self.world is stable. """

        auto = True

        while auto:

            self.past_iterations.append(self.world.stringify())
            self.advance_to_next_generation()

            if self.world.stringify() in self.past_iterations[-2:]:
                auto = False
        


    def exec(self):
        """ Run primary Game Loop. """

        print("""
  _______      ___      .___  ___.  _______      ______    _______     __       __   _______  _______ 
 /  _____|    /   \     |   \/   | |   ____|    /  __  \  |   ____|   |  |     |  | |   ____||   ____|
|  |  __     /  ^  \    |  \  /  | |  |__      |  |  |  | |  |__      |  |     |  | |  |__   |  |__   
|  | |_ |   /  /_\  \   |  |\/|  | |   __|     |  |  |  | |   __|     |  |     |  | |   __|  |   __|  
|  |__| |  /  _____  \  |  |  |  | |  |____    |  `--'  | |  |        |  `----.|  | |  |     |  |____ 
 \______| /__/     \__\ |__|  |__| |_______|    \______/  |__|        |_______||__| |__|     |_______|
 ------------------------------------------------------------------------------------------------------
 Created by John Conway""")

        self.help_menu()
        print(self.world)

        command = ""

        while command != "e":
            command, optional_parameters = self.main_menu()
            self.run_command(command, optional_parameters)

        print("\nThanks for playing!\nProgrammed by Ian Kollipara")
    
    def main_menu(self):
        """ Display Simulation's command menu. """

        command = ""

        while command not in self.simulation_actions.keys():
            print("[s]im | s[k]ip | [a]dvance | a[u]to | [p]opulate | [c]reate | sa[v]e | [l]oad | [t]orus | [h]elp | [e]xit")
            command = input().lower()
            optional_parameters = command[1:].lower().strip() if len(command) > 1 else None
            command = command[0].lower()
        
        return command, optional_parameters
    
    def run_command(self, command, optional_parameters):
        """ Run the given command with the optional_parameters. 
        
        Parameters
        command  character used to index the self.simulation_action dictionary
        optional_parameters  number used in commands
        """

        if optional_parameters is None:
            optional_parameters = self.get_parameters(command)
        
        self.simulation_actions[command](optional_parameters)

    def get_parameters(self, command):
        """ Get command parameters to run. 
        
        Parameters
        command  command used to index parameter options
        """

        return_val = 0

        if command in  ['s', 'k']:
            return_val = get_integer("To what generation? ")
        
        elif command == 'p':
            return_val = get_integer("What Percent? ")
        
        elif command == 'c':
            return_val = input("What size (Use a space as a seperator)? ")
        
        elif command == 's':
            return_val = input("What is the save name? ")
        
        elif command == 'l':
            print(listdir('Saves'))
            return_val = input("What file to load? ")
        
        elif command == 't':
            return_val = input("On or Off? ").lower()

        else:
            return_val = None
        
        return return_val