import unittest
from World import World
from Cell import Cell


class World_Case_Test(unittest.TestCase):
    def test_creation(self):
        world = World(5, 5)
        self.assertIsInstance(world, World)
        world.create_cells()
        for line in world.cells:
            for cell in line:
                self.assertIsInstance(cell, Cell)

    def test_populate(self):
        world = World(5, 5)
        world.populate(100)
        for line in world.cells:
            for cell in line:
                if cell.column == 0:
                    pass
                elif cell.column > world.columns:
                    pass
                elif cell.row > world.rows:
                    pass
                elif cell.row == 0:
                    pass
                else:
                    self.assertTrue(cell.status)
        world.reset()
        world.populate(0)
        for line in world.cells:
            for cell in line:
                self.assertFalse(cell.status)
        world.reset()
        world.populate()
        testNo = 0
        for line in world.cells:
            for cell in line:
                if cell.status:
                    testNo += 1
                else:
                    pass
        self.assertEqual(testNo, len(world)*.4)

    def test_irregular_world_creation(self):
        world = World(34, 2)
        self.assertIsInstance(world, World)
        self.assertEqual(world.rows, 34)
        self.assertEqual(world.columns, 2)
        for line in world.cells:
            for cell in line:
                self.assertIsInstance(cell, Cell)

    def test_neighbor_count(self):
        world = World(5, 5)
        world.create_cells()
        world.find_neighbors()
        for line in world.cells:
            for cell in line:
                livingNeighbors = len(cell.neighbors)
                self.assertTrue(livingNeighbors in [3, 8, 5])

    def test_irregular_neighbor_count(self):
        world = World(7, 12)
        world.create_cells()
        world.find_neighbors()
        for line in world.cells:
            for cell in line:
                livingNeighbors = len(cell.neighbors)
                self.assertTrue(livingNeighbors in [3, 5, 8])


    def test_next_gen(self):
        world = World(3, 3)
        world.create_cells()
        world.find_neighbors()
        world.populate(100)
        world.next_gen()
        alive = 0
        for line in world.cells:
            for cell in line:
                if cell.status:
                    alive += 1
                else:
                    pass
        self.assertEqual(alive, 4)

    def test_regen(self):
        world = World(3, 3)
        world.find_neighbors()
        world.cells[0][1].live()
        world.cells[1][0].live()
        world.next_gen()
        self.assertFalse(world.cells[0][0].status)
        world.cells[0][1].live()
        world.cells[1][0].live()
        world.cells[1][1].live()
        world.next_gen()
        self.assertTrue(world.cells[0][0].status)


if __name__ == '__main__':
    unittest.main()
