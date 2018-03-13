class Cell(object):
    def __init__(self, world, name, status=False):
        self.status = status
        self.world = world
        self.name = name

    def __str__(self):
        cellStr = ''
        if self.status:
            cellStr = 'X'
        else:
            cellStr = ' '
        return cellStr