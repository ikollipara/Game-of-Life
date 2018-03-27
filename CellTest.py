import unittest
from Cell import Cell
from World import World
from random import *


class Cell_Test_Case(unittest.TestCase):
    def test_creation(self):
        cell = Cell(None, 1, 1)
        self.assertIsInstance(cell, Cell)

    def test_multiple_cells(self):
        testCells = []
        for _ in range(4):
            cell = Cell(None, 1, _)
            testCells.append(cell)
        for cell in testCells:
            self.assertIsInstance(cell, Cell)
            self.assertFalse(cell.status)
            self.assertEqual(cell.y, 1)

    def test_live(self):
        cell = Cell(None, 0, 0)
        self.assertFalse(cell.status)
        cell.live()
        self.assertTrue(cell.status)

    def test_die(self):
        cell = Cell(None, 0, 0, True)
        self.assertTrue(cell.status)
        cell.die()
        self.assertFalse(cell.status)

    def test_neighbors(self):
        testCell = Cell(None, 0, 0)
        neighbors = []
        choices = [True, False]
        for _ in list(range(5)):
            choice = choices[randint(0, 1)]
            cell = Cell(None, 0, 0, choice)
            neighbors.append(cell)
        testCell.assign_neighbors(neighbors)
        self.assertIsNotNone(testCell.neighbors)
        livNeighbors = testCell.living_neighbors()
        self.assertEqual(livNeighbors, 5)

    def test_next_status(self):
        testCell = Cell(None, 0, 0)
        self.assertFalse(testCell.status)
        testCell.assign_next_status(True)
        testCell.next_status()
        self.assertTrue(testCell.status)

if __name__ == '__main__':
    unittest.main()
