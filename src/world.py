# src/world.py
# Ian Kollipara
# 2020.02.09
# World Class used in JCGoL
# 
# Usage
# from world import World

# Imports
from cell import Cell
from random import shuffle


class World:
    """ Implement a World Class for use in John Conway's Game of Life. 
    
    World contains all the cells and can be saved to a string.
    """

    # Instance Variables (public)
    # cell_matrix  A List of Lists of Cells 
    # size         Tuple of world size (row, columns)
    # is_torus     Boolean that tells if the world wraps into a sphere

    CELL_TOO_MANY = 4
    CELL_TOO_FEW = 2
    CELL_ALIVE_AGAIN = 3

    def __init__(self, size=(20, 60), population_rate=40, cell_matrix=None):
        """ __init__() create a World object. 
        
        Parameters
        size             Optional Tuple used to generate world size
        population_rate  Optional integer used for population generation
        cell_matrix      Optional List of Lists of Cells used to create world from save

        Usage
        w = World()
        print(w)
        print(w.stringify())
        w.advance_generation()
        print(w)
        """

        self.is_torus = False
        self.size = size
        self.cell_matrix = cell_matrix if cell_matrix is not None else self.init_cells(population_rate)
    
    def init_cells(self, population_rate):
        """ Generate a cell_matrix from given population_rate.
        
        Parameters
        population_rate  Integer used to find percent alive for cells. (population_rate/100)
        """

        percent_alive = ((self.size[0] * self.size[1]) * (population_rate/100))
        
        # Uses list comprehension to create a matrix of cells based on given size
        cell_matrix = [[Cell((row, column)) for column in range(self.size[1])] for row in range(self.size[0])]

        self.set_cell_matrix_neighbors(cell_matrix)

        cell_locations = []

        for row in cell_matrix:
            for cell in row:
                cell_locations.append(cell.location)

        shuffle(cell_locations)

        while percent_alive != 0:
            row, column = cell_locations.pop()
            cell_matrix[row][column].current_status = True
            percent_alive -= 1
        
        return cell_matrix

    def set_cell_matrix_neighbors(self, cell_matrix):
        """ Set each cell's neighbors. 
        
        Parameters
        cell_matrix  A List of Lists of Cells
        """

        for row in cell_matrix:

            for cell in row:

                cell_neighbors = []
                neighbors = [(1,-1), (1,0), (1,1), 
                             (0,-1),        (0,1), 
                            (-1,-1),(-1,0), (-1,1)]

                if not self.is_torus:

                    if cell.location[0] == 0:
                        neighbors.remove((-1,-1))
                        neighbors.remove((-1,0))
                        neighbors.remove((-1,1))

                    elif cell.location[1] == 0:
                        neighbors.remove((-1,-1))
                        neighbors.remove((0,-1))
                        neighbors.remove((1,-1))

                    elif cell.location[0] == self.size[0]-1:
                        neighbors.remove((1,-1))
                        neighbors.remove((1,0))
                        neighbors.remove((1,1))

                    elif cell.location[1] == self.size[1]-1:
                        neighbors.remove((-1,1))
                        neighbors.remove((0,1))
                        neighbors.remove((1,1))

                for neighbor in neighbors:

                    line, column = (cell.location[0] + neighbor[0]), (cell.location[1] + neighbor[1])

                    if line >= self.size[0]:
                        line = 0

                    if column >= self.size[1]:
                        column = 0
                    
                    cell_neighbors.append(cell_matrix[line][column])

                cell.neighbors = cell_neighbors



    def advance_generation(self):
        """ Advance world to next generation. """

        next_statuses = []

        for row in self.cell_matrix:

            next_status_line = []

            for cell in row:

                cell_living_neighbors = cell.current_living_neighbors_count()
            
                if cell_living_neighbors == World.CELL_ALIVE_AGAIN:
                    next_status_line.append(True)

                elif cell_living_neighbors in range(World.CELL_TOO_FEW, World.CELL_TOO_MANY):
                    next_status_line.append(cell.current_status)

                elif cell_living_neighbors >= World.CELL_TOO_MANY:
                    next_status_line.append(False)

                elif cell_living_neighbors < World.CELL_TOO_FEW:
                    next_status_line.append(False)

            next_statuses.append(next_status_line)
        
        for row, line in enumerate(next_statuses):

            for column, status in enumerate(line):

                self.cell_matrix[row][column].current_status = status

    def stringify(self):
        """ Return a string version of World. """
        
        string = ""

        for row in self.cell_matrix:

            for cell in row:

                string += "1" if cell.current_status else "0"
        
        string+="N"

        return string

    @classmethod
    def from_save_file(cls, filename):
        """ Create world instance from filename given. 
        
        Parameters
        filename  String used to load file from
        """

        with open(f"Saves/{filename}") as save:
            world_string = save.read()
        
        cell_matrix = []

        for char in world_string:

            line = []
            column = 0

            if char == "1":
                line.append(Cell((len(cell_matrix), column), True))

            elif char == "0":
                line.append(Cell((len(cell_matrix), column), False))

            elif char == "N":
                cell_matrix.append(line)
                line = []
                column = 0
        
        return cls(cell_matrix=cell_matrix)


    def __str__(self):
        """ Return display string of World. """
        
        world_string = ""

        for row in self.cell_matrix:
            
            for cell in row:

                world_string += str(cell)
        
            world_string += '\n'
        
        return world_string