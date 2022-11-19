class Sudoku():
    """
    A class to defind basic information of a Sudoku puzzle.
    """
    def __init__(self, initial_grid):
        """ 
        Initialize the Sudoku puzzle.
        Arguments:
            - initialGrid (str): string representing the sudoku grid
            - Ex. the most difficult sudoku
            - '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
        """
        if len(initial_grid) != 81:
            raise Exception("Grid must be 81 characters")

        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits

        self.setPuzzle()
        self.initial_grid = initial_grid
        self.grid = self.str2grid()     # disc with initial values
        self.values = self.grid2value() # disc with possible values
        
    @staticmethod
    def cross(A, B):
        """
        Cross product of elements in A and elements in B 
        Arguments:
            - A (str): str contents rows
            - B (str): str contents cols   
        Returns:
            - C (list): list content position tag ["A1","A2", ... "I9"]
        """
        C = [a + b for a in A for b in B]
        return C

    def setPuzzle(self):
        """
        Set helpful attributes about the sudoku puzzle
        """
        # row, column and box units
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.col_units = [self.cross(self.rows, c) for c in self.cols]
        self.box_units = [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        self.unit_list = self.row_units + self.col_units + self.box_units

        # cells is a list of all the positions
        # units is a dict of all related rows, columns and boxs for each position
        # peers is a dict of all related positions for each position
        self.cells = self.cross(self.rows,self.cols)
        self.units = dict((s, [u for u in self.unit_list if s in u]) for s in self.cells)
        self.peers = dict((s, set(sum(self.units[s],[])) - set([s])) for s in self.cells)

    def str2grid(self, grid=None):
        """
        Convert input Sudoku str into a dict with '0' for empty.
        Arguments:
            - grid (str): string representing the sudoku grid
            - Ex. '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
        Returns:
            - values (dict): cells map to their values strings (i.e. 'A1' => '8')
            - Empty values will be set to '0'
        """
        # Use initial grid if without input new grid str
        if grid is None:
            grid = self.initial_grid

        grid_dict = {}
        for val, key in zip(grid, self.cells):
            if val in '0.':
                grid_dict[key] = '0'
            else:
                grid_dict[key] = val
        return grid_dict

    def grid2value(self, grid=None):
        """
        Replace empty value with possible values in str.
        Arguments:
            - grid (dict): cells map to their values strings
            - Ex. {'A1':'8', 'A2':'0', ...}
        Returns:
            - values (dict): cells map to their values strings 
            - Empty values will be set to '123456789'
            - 'A2' => '123456789'
        """
        # Use self.grid if without input new grid dict
        if grid is None:
            grid = self.grid
        grid_dict = {}
        for key in grid:
            if grid[key] in '0.':
                grid_dict[key] = self.digits
            else:
                grid_dict[key] = grid[key]
        return grid_dict

    def values2str(self, values=None):
        """
        Convert the dictionary board representation to as string.
        Arguments:
            - values (dict): cells map to their values strings 
            - (i.e. 'A1' => '8')
        Returns:
            - grid (str): string representing the sudoku grid
            - Ex. '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
        """
        if values is None:
            values = self.values

        res = []
        for r in self.rows:
            for c in self.cols:
                v = values[r + c]
                res.append(v if len(v) == 1 else '.')
        return ''.join(res)
        
    def isSolved(self, values=None):
        """ 
        Determine if the puzzle has been solved.
        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - solved (boolean): whether or not the puzzle is solved
        """
        if values is None:
            values = self.values

        # Each cell has only one number
        allReduced = all(len(values[cell]) == 1 for cell in self.cells)
        if not allReduced: return False

        # Check if there is only 1-9 for each row, col and box
        for unit in self.unit_list:
            required_digits = self.digits
            for cell in unit:
                required_digits = required_digits.replace(values[cell], '')
            if len(required_digits) != 0:
                return False
        return True

    def display(self, values=None):
        """
        Display these values as a 2-D grid. In formate of:
        8 0 0 |0 0 0 |0 0 0 
        0 0 3 |6 0 0 |0 0 0
        0 7 0 |0 9 0 |2 0 0
        ------+------+------
        0 5 0 |0 0 7 |0 0 0
        0 0 0 |0 4 5 |7 0 0
        0 0 0 |1 0 0 |0 3 0
        ------+------+------
        0 0 1 |0 0 0 |0 6 8
        0 0 8 |5 0 0 |0 1 0
        0 9 0 |0 0 0 |4 0 0

        Arguments:
            - values (dict): cells map to their values strings
        Returns:
            - 2-D grid display on screen
        """
        # Use self.values if without input new value dict
        if values is None:
            values = self.values

        width = 1 + max(len(values[s]) for s in self.cells)
        line = '+'.join(['-' * (width * 3)] * 3)

        for r in self.rows:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self.cols))
            if r in 'CF': 
                print(line)
        return
        

# if __name__ == '__main__':
#     grid1 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
#     puzzle = Sudoku(grid1)
#     puzzle.display()

