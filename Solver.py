from Sudoku import Sudoku
import time

class Solver():
    """
    A class that solve sudoku puzzle
    """
    def setSolver(self, puzzle):
        """
        Initialize the solver based on the rules of sudoku
        Arguments:
            - puzzle(object): the sudoku puzzle which need to be solved
        """
        if not isinstance(puzzle, Sudoku):
            raise Exception("The puzzle needs to be an instance of Sudoku")

        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits

        self.unit_list = puzzle.unit_list
        self.cells = puzzle.cells
        self.units = puzzle.units
        self.peers = puzzle.peers

    def eliminate(self, values):
        """
        Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected.
        Arguments:
            - values (dict): cells map to their values strings (i.e. 'A1' => '135')
        Returns:
            - values (dict): updated values dict with the digit removed from the box
        """
        for cell, value in values.items():
            if len(value) == 1:
                for peer in self.peers[cell]:
                    values = self.removeDigit(values, peer, value)
        return values

    @staticmethod
    def removeDigit(values, cell, digit):
        """
        Remove a digit from the possible values of a box.
        Arguments:
            - values (dict): cells map to their values strings
            - box (str): the box to remove the digit from
            - digit (str): the digit to remove from the box
        Returns:
            - values (dict): updated values dict with the digit removed from the box
        """
        values[cell] = values[cell].replace(digit, '')
        return values

    def isValid(self, values, cell):
        """
        Determine if the number is valid.
        Arguments:
            - values (dict): cells map to their values strings
            - cell (str): the position of cell need to check
        Returns:
            - valid (boolean): whether the number is valid or not
        """
        for peer in self.peers[cell]:
            if len(values[peer]) == 1 and values[cell] == values[peer]:
                return False
        return True


class Solver_Backtrack(Solver):
    """
    A class to solve sudoku puzzle by backtrack method
    Inherit the methods and properties from its parent
    """
    def __init__(self, puzzle):
        Solver.setSolver(self, puzzle)
        self.guessTime = 0

    def solve(self, puzzle, isDisplay=True):
        """
        Use backtrack method to solve the puzzle.
        Arguments:
            - isDisplay (boolean): confirm that if need display
        Returns:
            - values (dict): cells map to their values strings
        """       
        start = time.process_time()
        values = puzzle.values
        puzzle.values = self.backtrack(values)
        t1 = time.process_time() - start

        if puzzle.isSolved():
            message = "The puzzle successfully solved by backtrack method, \nwith " + str(self.guessTime) + " guesses and " +str(t1)+" secs!"
        else:
            message = "The solver failed!"

        if isDisplay:
            print(message)
            #puzzle.display()

 
    def backtrack(self, values):
        """ 
        Use backtrack method to solve the puzzle.
        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): cells map to their values strings
        """
        # The puzzle is solved
        if all(len(values[s]) == 1 for s in self.cells):
            return values

        # Target all unsolved cells
        for cell in values.keys():
            if len(values[cell]) > 1:
                # Try all possible values in the cell
                for value in values[cell]:
                    temp = values.copy() # make a copy
                    temp[cell] = value # make a guess
                    self.guessTime += 1 # count guess time
                    # Check next cell if valid, try next possible value if not valid
                    if self.isValid(temp, cell) == True:
                        nextCell = self.backtrack(temp)
                        # If true return fixed value, if false try next possible value
                        if nextCell:
                            return nextCell
                # Backtrack if all possible values are invalid
                return False

class Solver_Arc(Solver):
    """
    A class to solve sudoku puzzle by backtrack method with Arc consistency filter
    Inherit the methods and properties from its parent
    """
    def __init__(self, puzzle):
        Solver.setSolver(self, puzzle)
        self.guessTime = 0

    def solve(self, puzzle, isDisplay=True):
        """
        Use backtrack method with Arc consistency filter to solve the puzzle.
        Arguments:
            - puzzle (object): cells map to their values strings
            - isDisplay (boolean): confirm that if need display
        Returns:
            - values (dict): cells map to their values strings
        """        
        # Apply the filter to reduce the possible values for all cells
        start = time.process_time()
        values = self.eliminate(puzzle.values)
        puzzle.values = self.backtrack(values)
        t2 = time.process_time() - start

        if puzzle.isSolved():
            message = "The puzzle successfully solved by backtrack method with Arc consistency filter, \nwith " + str(self.guessTime) + " guesses and " +str(t2)+" secs!"
        else:
            message = "The solver failed!"

        if isDisplay:
            print(message)
            #puzzle.display()

 
    def backtrack(self, values):
        """ 
        Use backtrack method to solve the puzzle.
        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): cells map to their values strings
        """
        # The puzzle is solved
        if all(len(values[s]) == 1 for s in self.cells):
            return values

        # Target all unsolved cells
        for cell in values.keys():
            if len(values[cell]) > 1:
                # Try all possible values in the cell
                for value in values[cell]:
                    temp = values.copy() # make a copy
                    temp[cell] = value # make a guess
                    self.guessTime += 1 # count guess time
                    # Check next cell if valid, try next possible value if not valid
                    if self.isValid(temp, cell) == True:
                        nextCell = self.backtrack(temp)
                        # If true return fixed value, if false try next possible value
                        if nextCell:
                            return nextCell
                # Backtrack if all possible values are invalid
                return False

class Solver_Human(Solver):
    """
    A class to solve sudoku puzzle by backtrack method
    Inherit the methods and properties from its parent
    """
    def __init__(self, puzzle):
        Solver.setSolver(self, puzzle)
        self.guessTime = 0

    def onlyChoice(self, values):
        """
        Apply the only choice strategy to a Sudoku puzzle.
        If only one cell in a unit allows a certain digit, 
        then that cell must be assigned that digit.
        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): the values dict with only choice values solved
        """
        # Check each cell and their related cells
        for unit in self.unit_list:
            for digit in self.digits:
                remainder = [cell for cell in unit if digit in values[cell]]
                if len(remainder) == 1:
                    values[remainder[0]] = digit
        return values

    def nakedTwins(self, values):
        """ 
        Eliminate values using the naked twins strategy.
        Twins are the length two and occur exactly twice in the unit.
        Args:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): the values dict with naked twins eliminated
        """
        for unit in self.unit_list:
            # Find the current twins for a unit
            unit_values = [values[cell] for cell in unit]
            twin_values = [value for value in unit_values if unit_values.count(value) == 2 and len(value) == 2]
            # Remove twins values from a unit
            for cell in unit:
                if values[cell] in twin_values:
                    continue
                for twin in twin_values:
                    for digit in twin:
                        values = self.removeDigit(values, cell, digit)

        return values


    def solve(self, puzzle, isDisplay=True):
        """
        Use backtrack method to solve the puzzle.
        Arguments:
            - isDisplay (boolean): confirm that if need display
        Returns:
            - values (dict): cells map to their values strings
        """    

        start = time.process_time()
        values = puzzle.values
        puzzle.values = self.backtrack(values)
        t3 = time.process_time() - start

        if puzzle.isSolved():
            message = "The puzzle successfully solved by human method, \nwith " + str(self.guessTime) + " guesses and " +str(t3)+" secs!"
        else:
            message = "The solver failed!"

        if isDisplay:
            print(message)
            #print(str(self.guessTime), str(t3))
            #puzzle.display()

    def backtrack(self, values):
        """ 
        Use backtrack method to solve the puzzle.
        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): cells map to their values strings
        """
        values = self.simplify(values)

        if values is False:
            return False ## Failed earlier
        # The puzzle is solved
        if all(len(values[s]) == 1 for s in self.cells):
            return values

        # Pick the cell with less possible values to guess 
        cell = min(cell for cell in self.cells if len(values[cell]) > 1)
        # Try all possible values in the cell
        for value in values[cell]:
            temp = values.copy() # make a copy
            temp[cell] = value # make a guess
            self.guessTime += 1 # count guess time
            # Check next cell if valid, try next possible value if not valid
            nextCell = self.backtrack(temp)
            # If true return fixed value, if false try next possible value
            if nextCell:
                return nextCell
        # # Backtrack if all possible values are invalid
        # return False

    def simplify(self, values):
        """ 
        Eliminate values using the naked twins strategy.
        Twins are the length two and occur exactly twice in the unit.
        Args:
            - values (dict): cells map to their values strings
        Returns:
            - values (dict): the values dict after application of the constraint strategies
        """    
        # Repeatedly applying all constraint strategies.
        stalled = False
        while not stalled:
            beforeFilter = len([box for box in values.keys() if len(values[box]) == 1])
            # Apply the filter to reduce the possible values for all cells
            values = self.eliminate(values)
            values = self.onlyChoice(values)
            values = self.nakedTwins(values)

            afterFilter = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = (beforeFilter == afterFilter)
            
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

