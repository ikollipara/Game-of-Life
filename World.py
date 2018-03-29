from Cell import Cell
from random import *

class World(object):
    AliveAgain = 3
    TooMany = 3
    TooFew = 2
    def __init__(self, rows, columns, cells=None):
        self.rows = rows
        self.columns = columns
        if cells != None:
            self.cells = cells
        else:
            self.cells = self.create_cells()
        self.torus = False
        self.pastVersions = []
        self.currentGen = 0
        self.name = 'untitled'

    def create_cells(self):
        cells = []
        rows = 0
        columns = 0
        for row in list(range(self.rows)):
            line = []
            for _ in list(range(self.columns)):
                cell = Cell(None, rows, columns)
                line.append(cell)
                columns += 1
            cells.append(line)
            rows += 1
            columns = 0
        return cells

    def TorusOn(self):
        self.torus = True
        self.find_neighbors()

    def TorusOff(self):
        self.torus = False
        self.find_neighbors()

    def reset(self):
        """Purely for debugging and testing purposes"""
        for line in self.cells:
            for cell in line:
                cell.status = False

    def find_neighbors(self):
        for line in self.cells:
            for cell in line:
                neigbors = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 1),
                            (1, -1), (1, 0), (1, 1)]
                neigbors = set(neigbors)
                cellNeighbors = []
                if not self.torus:
                    if cell.row == 0:
                        neigbors.discard((-1, -1))
                        neigbors.discard((-1, 0))
                        neigbors.discard((-1, 1))
                    if cell.row == self.rows-1:
                        neigbors.discard((1, -1))
                        neigbors.discard((1, 0))
                        neigbors.discard((1, 1))
                    if cell.column == 0:
                        neigbors.discard((-1, -1))
                        neigbors.discard((0, -1))
                        neigbors.discard((1, -1))
                    if cell.column == self.columns-1:
                        neigbors.discard((-1, 1))
                        neigbors.discard((0, 1))
                        neigbors.discard((1,1))
                for neighbor in neigbors:
                    row = cell.row + neighbor[0]
                    column = cell.column + neighbor[1]
                    if row >= self.rows:
                        row = 0
                    if column >= self.columns:
                        column = 0
                    cellNeighbors.append(self.cells[row][column])
                cell.assign_neighbors(cellNeighbors)

    def populate(self, percent=40):
        """Randomly populates the world according to the percent given"""
        cellLocations = []
        for line in self.cells:
            for cell in line:
                location = []
                location.append(cell.column)
                location.append(cell.row)
                cellLocations.append(location)
        aliveCells = int(len(self) * (percent/100))
        shuffle(cellLocations)
        for _ in range(aliveCells):
            x, y = cellLocations.pop()
            self.cells[y][x].live()

    def __len__(self):
        return self.columns * self.rows

    def next_gen(self):
        """Generates the next generation"""
        for line in self.cells:
            for cell in line:
                livNeighbors = cell.living_neighbors()
                if livNeighbors == World.AliveAgain:
                    cell.assign_next_status(True)
                elif livNeighbors in list(range(World.TooFew, World.TooMany+1)):
                    cell.assign_next_status(cell.status)
                elif livNeighbors > World.TooMany:
                    cell.assign_next_status(False)
                elif livNeighbors < World.TooFew:
                    cell.assign_next_status(False)
        for line in self.cells:
            for cell in line:
                cell.next_status()

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


def test():
    world = World.from_file('Long L.life')
    print(world.columns)
    print(world.rows)
    world.find_neighbors()
    print(len(world.cells[0][0].neighbors))
test()