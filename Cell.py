class Cell(object):
    deadChar = '\u2B1C'
    aliveChar = '\u2B1B'
    def __init__(self, world, row, column, status=False):
        self.status = status
        self.world = world
        self.column = column
        self.row = row
        self.nextStatus = None
        self.neighbors = []

    def assign_neighbors(self, neighborList):
        """Sets self.neighbors to the list provided"""
        self.neighbors = neighborList

    def live(self):
        """Changes the cell's status to True"""
        self.status = True

    def die(self):
        """Changes the cell's status to False"""
        self.status = False

    def living_neighbors(self):
        """Calculates the cell's living neighbors based from self.neighbors"""
        living = 0
        for cell in self.neighbors:
            if cell.status:
                living += 1
            else:
                pass
        return living

    def next_status(self):
        self.status = self.nextStatus

    def assign_next_status(self, bool):
        self.nextStatus = bool

    def __str__(self):
        if self.status:
            return Cell.aliveChar
        else:
            return Cell.deadChar
