from Cell import Cell
from random import *
from time import sleep

class World(object):
    def __init__(self, row, column, cells=None):
        self.columns = column
        self.rows = row
        if cells == None:
            self.cells = self.create()
        else:
            self.cells = cells
        self.name = "{} x {} World".format(self.columns, self.rows)

    def create(self):
        """Generates the cells with the parameters given by the User"""
        cells = []
        #
        # Row corresponds with the Y-Axis
        # Column corresponds with the X-Axis
        #
        columnNumber = 0
        rowNumber = 0
        for line in range(self.rows):
            line = []
            for _ in range(self.columns):
                cell = Cell(self, rowNumber, columnNumber)
                line.append(cell)
                columnNumber += 1
            rowNumber += 1
            columnNumber = 0
            cells.append(line)
        return cells

    def populate(self, percent=40):
        """Randomly populates the world according to the percent given"""
        cellLocations = []
        for line in self.cells:
            for cell in line:
                location = []
                location.append(cell.x)
                location.append(cell.y)
                cellLocations.append(location)
        aliveCells = int(len(self) * (percent/100))
        shuffle(cellLocations)
        for _ in range(aliveCells):
            x, y = cellLocations.pop()
            self.cells[y][x].live()


    def reset(self):
        """Purely for debugging and testing purposes"""
        for line in self.cells:
            for cell in line:
                cell.status = False

    def set_neighbors(self):
        """Sets the Neighbors for each cell"""
        for line in self.cells:
            for cell in line:
                neighbors = []
                if cell.y == 0:
                    if cell.x == 0:
                        neighbors.append(self.cells[0][1])
                        neighbors.append(self.cells[1][0])
                        neighbors.append(self.cells[1][1])
                    elif cell.x == self.columns-1:
                        neighbors.append(self.cells[0][cell.x-1])
                        neighbors.append(self.cells[1][cell.x])
                        neighbors.append(self.cells[1][cell.x-1])
                    else:
                        neighbors.append(self.cells[0][cell.x+1])
                        neighbors.append(self.cells[0][cell.x-1])
                        neighbors.append(self.cells[1][cell.x])
                        neighbors.append(self.cells[1][cell.x+1])
                        neighbors.append(self.cells[1][cell.x-1])
                elif cell.y == self.rows-1:
                    if cell.x == 0:
                        neighbors.append(self.cells[cell.y][1])
                        neighbors.append(self.cells[cell.y-1][0])
                        neighbors.append(self.cells[cell.y-1][1])
                    elif cell.x == self.columns-1:
                        neighbors.append(self.cells[cell.y][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x])
                        neighbors.append(self.cells[cell.y-1][cell.x-1])
                    else:
                        neighbors.append(self.cells[cell.y][cell.x+1])
                        neighbors.append(self.cells[cell.y][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x])
                        neighbors.append(self.cells[cell.y-1][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x+1])
                else:
                    if cell.x == 0:
                        neighbors.append(self.cells[cell.y][1])
                        neighbors.append(self.cells[cell.y-1][0])
                        neighbors.append(self.cells[cell.y+1][0])
                        neighbors.append(self.cells[cell.y+1][1])
                        neighbors.append(self.cells[cell.y-1][1])
                    elif cell.x == self.columns-1:
                        neighbors.append(self.cells[cell.y][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x])
                        neighbors.append(self.cells[cell.y+1][cell.x])
                        neighbors.append(self.cells[cell.y+1][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x-1])
                    else:
                        neighbors.append(self.cells[cell.y][cell.x+1])
                        neighbors.append(self.cells[cell.y][cell.x-1])
                        neighbors.append(self.cells[cell.y+1][cell.x])
                        neighbors.append(self.cells[cell.y-1][cell.x])
                        neighbors.append(self.cells[cell.y+1][cell.x-1])
                        neighbors.append(self.cells[cell.y+1][cell.x+1])
                        neighbors.append(self.cells[cell.y-1][cell.x-1])
                        neighbors.append(self.cells[cell.y-1][cell.x+1])
                cell.assign_neighbors(neighbors)



    def next_gen(self):
        """Generates the next generation"""
        for line in self.cells:
            for cell in line:
                livNeighbors = cell.living_neighbors()
                if livNeighbors == 3:
                    cell.assign_next_status(True)
                elif livNeighbors in [2, 3]:
                    cell.assign_next_status(cell.status)
                elif livNeighbors > 3:
                    cell.assign_next_status(False)
                elif livNeighbors < 2:
                    cell.assign_next_status(False)
        for line in self.cells:
            for cell in line:
                cell.next_status()


    def __len__(self):
        return self.columns * self.rows

    def __str__(self):
        worldstr = ''
        for line in self.cells:
            for cell in line:
                worldstr += str(cell)
            worldstr += '\n'
        return worldstr

    @classmethod
    def from_file(cls, file):
        world = []
        rows = 0
        columns = 0
        with open(r'.\Saves\{}'.format(file), 'r') as worldSave:
            for line in worldSave:
                row = []
                cells = line.split(',')
                for byte in cells:
                    if byte == '1':
                        cell = Cell(None, rows, columns, True)
                        row.append(cell)
                    elif byte == '0':
                        cell = Cell(None, rows, columns)
                        row.append(cell)
                    elif byte == '\n':
                        pass
                    columns += 1
                world.append(row)
                rows += 1
                finalColumns = columns-1
                columns = 0
        fileWorld = cls(rows, finalColumns, cells=world)
        return fileWorld
