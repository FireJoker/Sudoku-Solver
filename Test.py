import unittest
from Sudoku import Sudoku
from Solver import *

grid1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
grid2 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'


class IntegerArithmeticTestCase(unittest.TestCase):  
        def testBacktrack(self):  # test method names begin with 'test'  
            puzzle = Sudoku(grid1)
            solver = Solver_Backtrack(puzzle)
            solver.solve(puzzle)
            self.assertTrue(puzzle.isSolved()) 

        def testArc(self):  
            puzzle = Sudoku(grid1)
            solver = Solver_Arc(puzzle)
            solver.solve(puzzle)
            self.assertTrue(puzzle.isSolved()) 

        def testHuman(self):  
            puzzle = Sudoku(grid1)
            solver = Solver_Human(puzzle)
            solver.solve(puzzle)
            self.assertTrue(puzzle.isSolved()) 

if __name__ == '__main__':  
    unittest.main()