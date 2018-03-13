from Cell import Cell
from random import *

class World(list):
    def __init__(self, x, y):
        super(World, self).__init__()
        names = ['Rachel', 'Ian', 'Nhu', 'Jacob', 'Zac', 'Collin', 'Tessa', 'Lloyd', 'Derek']
        Values = [True, False]
        for _ in range(y):
            line = []
            for _ in range(x):
                name = names[randint(0, len(names)-1)]
                status = Values[randint(0,1)]
                cell = Cell(self, name, status)
                line.append(cell)
            self.append(line)

    def adv_gen(self):
        pass

    def __str__(self):
        worldStr = ''
        for _ in range(len(self[0])*2):
            worldStr += '_'
        worldStr += '\n'
        for line in self:
            for cell in line:
                worldStr += '|'
                worldStr += str(cell)
            worldStr += '\n'
            for _ in range(len(self[0])*2):
                worldStr += '-'
            worldStr += '\n'
        return worldStr