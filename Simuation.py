from World import World
from getFunctions import *
from time import sleep
import os


class Simulation(object):
    def __init__(self):
        self.world = None
        self.auto = False

    def add_world(self, x, y):
        world = World(y, x)
        self.world = world

    # def main_menu(self):
    #     options = ['f', 'e', 'a', 'h', 'x']
    #     print("""[F]ile [E]dit [A]ctions [H]elp E[x]it""")
    #     command = input()
    #     command = command[0].lower()
    #     while command not in options:
    #         command = input()
    #         command = command[0].lower()
    #     if command == 'f':
    #         self.file_menu()
    #     elif command == 'e':
    #         self.edit_menu()
    #     elif command == 'a':
    #         self.action_menu()
    #     elif command == 'h':
    #         self.help()
    #     else:
    #         pass
    #
    # def file_menu(self):
    #     options = ['s', 'l', 'b']
    #     command = None
    #     while command != 'b':


    def menu(self):
        options = ['p', 'c', 's', 'k', 'r', 'v', 'l', 'a', 'e', 'h', 't']
        command = ''
        while command not in options:
            print("""[P]opulate [C]reate [S]im S[K]ip [R]eady-Made Worlds
    Sa[v]e [L]oad [A]dvance [T]orus [H]elp [E]xit""")
            command = input()
            if len(command) > 1:
                parameter = command[1:].strip()
            else:
                parameter = None
            command = command[0].lower()
        return command, parameter

    def run(self, command, parameter):
        if command == 'p':
            self.populate(parameter)
        elif command == 'c':
            self.create(parameter)
        elif command == 's':
            self.sim(parameter)
        elif command == 'k':
            self.skip(parameter)
        elif command == 'r':
            command = self.worlds_menu()
        elif command == 'a':
            self.world.next_gen()
            print(self.world)
        elif command == 't':
            self.torus(parameter)
        elif command == 'v':
            if parameter != None:
                saveName = parameter
            else:
                saveName = input('Please enter a filename: ')
            self.save(saveName)
        elif command == 'l':
            fileNames = os.listdir(path='.\Saves')
            if parameter != None:
                if parameter[-5:] != '.life':
                    parameter += '.life'
                else:
                    pass
                if parameter in fileNames:
                    self.load(parameter)
                else:
                    print("{} doesn't exist".format(parameter))
            else:
                for world in fileNames:
                    print(world)
                file = input()
                if file not in fileNames:
                    print("{} doesn't exist".format(file))
                else:
                    self.load(file)
        elif command == 'h':
            self.help()
        elif command == 'e':
            pass

    def torus(self, parameter):
        options = ['on', 'off']
        if parameter != None:
            if parameter.lower() in options:
                if parameter.lower() == 'on':
                    self.world.TorusOn()
                else:
                    self.world.TorusOff()
            else:
                print("Torus must be On or Off, not {}".format(parameter))
        else:
            command = input("On or Off? ")
            command = command.lower()
            while command  not in options:
                command = input("On or Off? ")
                command = command.lower()
            if command == 'on':
                self.world.TorusOn()
            else:
                self.world.TorusOff()
        self.world.find_neighbors()
        print(self.world)

    def populate(self, parameter):
        if parameter != None:
            percent = int(parameter)
        else:
            percent = get_integer("Please enter the percent: ")
        self.world.reset()
        self.world.populate(int(percent))
        self.world.find_neighbors()
        print(self.world)

    def create(self, parameter):
        if parameter != None:
            parts = parameter.split(' ')
            x = parts[0]
            y = parts[1]
        else:
            x = get_integer("Columns: ")
            y = get_integer("Rows: ")
        self.add_world(int(x), int(y))
        print(self.world)

    def sim(self, parameter):
        if parameter != None:
            gen = int(parameter)
        else:
            gen = get_integer("To what generation: ")
        for _ in list(range(int(gen))):
            self.world.next_gen()
            print(self.world)
            sleep(.1)

    def skip(self, parameter):
        if parameter != None:
            gen = int(parameter)
        else:
            gen = get_integer("To what generation: ")
        for _ in list(range(int(gen))):
            self.world.next_gen()
        print(self.world)

    def help(self):
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
        Ready-made Worlds   | Brings up a menu of Prebuilt Worlds with interesting patterns
        Save                | Save current world in a directory called "Saves"
        Load                | Loads the specified saved world from "Saves"
        Populate            | Repopulate the current world via a given percent
        Help                | Brings up this menu
        Torus               | Makes the edges solid when off, or connected when on
        Exit                | Quits the Program
        ----------------------------------------------------------------------------------------
        """)

    def worlds_menu(self):
        options = ['l', 'g', 's', 'p', 'o']
        print("[L]ong L [G]lider [S]paceship [P]ulsar G[o]sper Gun")
        command = input()
        choice = command[0].lower()
        while choice not in options:
            print("[L]ong L [G]lider [S]paceship [P]ulsar G[o]sper Gun")
            command = input()
            choice = command[0].lower()
        if choice == 'l':
            item = 'Long L.life'
        elif choice == 'g':
            item = 'Glider.life'
        elif choice == 's':
            item = 'Spaceship.life'
        elif choice == 'p':
            item = 'Pulsar.life'
        elif choice == 'o':
            item = 'Gosper Gun.life'
        self.load(item)

    def load(self, worldSave):
        world = World.from_file(worldSave)
        self.world = world
        self.world.find_neighbors()
        print(self.world)

    def save(self, saveName):
        fileNames = os.listdir(path='.\Saves')
        replace = 'no'
        extension = 'life'
        if '.' in saveName:
            fullName = saveName.split('.')
            if fullName[1] != extension:
                saveName = fullName[0] + '.life'
            else:
                pass
        else:
            saveName += '.life'
        while saveName in fileNames and replace == 'no':
            print('{} already exists'.format(saveName))
            replace = get_yes_no("Do you want to replace {}? ".format(saveName))
            if replace == 'no':
                saveName = input("Please enter in new Filename: ")
                if '.' in saveName:
                    fullName = saveName.split('.')
                    if fullName[1] != extension:
                        saveName = fullName[0] + '.life'
                    else:
                        pass
                else:
                    saveName += '.life'
        with open(r'.\Saves\{}'.format(saveName), 'w+') as newWorld:
            fileline = ''
            for line in self.world.cells:
                for cell in line:
                    if cell.status:
                        byte = '1'
                    else:
                        byte = '0'
                    fileline += byte + ','
                fileline += '\n'
            newWorld.write(fileline)
        self.world.name = saveName

    def intro(self):
        print("""
  _______      ___      .___  ___.  _______      ______    _______     __       __   _______  _______ 
 /  _____|    /   \     |   \/   | |   ____|    /  __  \  |   ____|   |  |     |  | |   ____||   ____|
|  |  __     /  ^  \    |  \  /  | |  |__      |  |  |  | |  |__      |  |     |  | |  |__   |  |__   
|  | |_ |   /  /_\  \   |  |\/|  | |   __|     |  |  |  | |   __|     |  |     |  | |   __|  |   __|  
|  |__| |  /  _____  \  |  |  |  | |  |____    |  `--'  | |  |        |  `----.|  | |  |     |  |____ 
 \______| /__/     \__\ |__|  |__| |_______|    \______/  |__|        |_______||__| |__|     |_______|
 ------------------------------------------------------------------------------------------------------
 Created by John Conway""")

    def outro(self):
        print(""" 
Thanks for playing!
Programmed by Ian Kollipara""")
