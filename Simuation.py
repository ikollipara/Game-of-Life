from World import World
class Simulation(object):
    def __init__(self, name=False):
        self.world = None
        self.name = name
        self.size = []

    def add_world(self, x, y):
        self.world = World(x, y)
        self.size.append(x)
        self.size.append(y)

    def name_game(self, name=None):
        if name == None:
            self.name = "{} x {} Board".format(self.size[0], self.size[1])
        else:
            self.name = name

    def __str__(self):
        simStr = """
Name: {}
{}""".format(self.name, str(self.world))
        return simStr


def test():
    sim = Simulation()
    sim.add_world(34, 2)
    sim.name_game()
    print(str(sim))

test()