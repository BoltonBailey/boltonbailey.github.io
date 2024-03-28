import itertools

N = None

# this file is a work in progress
# TODO Implement the suggestion from my minesweeper post


class MinesweeperBoard:
    def __init__(self, array):
        self.board = array

        self.rows = len(self)
        self.cols = len(self[0])

    def all_squares(self):
        return frozenset([(i, j) for i in range(rows) for j in range(cols)])

    def __contains__(self, coords):
        i, j = coords
        return 0 <= i < self.rows and 0 <= j < self.cols

    def adjacent_squares(self, i: int, j: int):
        """Set of squares adjacent to (i, j)

        Parameters
        ----------
        i : int
            [description]
        j : int
            [description]

        Returns
        -------
        [type]
            [description]
        """
        allcoords = [(i + di, j + dj)
                     for di in [-1, 0, 1] for dj in [-1, 0, 1]]
        return frozenset([coords for coords in allcoords if coords in self])

    def get_probabilities(self, total_mines=None):
        """Determines constraints for each square being a mine.
        """

        # Map from frozensets of coordinate-pairs to numbers of mines
        constraints = {}

        if total_mines:
            constraints[self.all_squares()] = total_mines

        for i in range(rows):
            for j in range(cols):
                # When we see a numbered square...
                if not self[i][j] is None:
                    # That square has no mine in it
                    constraints[frozenset([(i, j)])] = 0
                    # The surrounding squares have mine_count mines
                    mine_count = self[i][j]
                    constraints[self.adjacent_squares(i, j)] = mine_count

        # Map from squares to constraints on that square
        squares_to_constraints = {
            square: set() for square in constraint for constraint in constraints
        }

        # Populate squares_to_constraints
        for constraint in constraints:
            for square in constraint:
                squares_to_constraints[square].add(constraint)

        # Now that all of the constraints are added, we try to simplify them
        # That is, we reduce the set of constraints to one where
        # * no constraint set occurs as a subset of another
        # * squares that are forced to be mines/empty are denoted so.
        done = False
        while not done:
            # Temporarily set done flag to True. If we find we have more
            # simplification to do, we will turn this back to False
            done = True

            # Check for subsets among constraints, using the squares to
            # constraints map
            for square in iter(squares_to_constraints):
                for c1, c2 in itertools.permutations(squares_to_constraints[square], 2):
                    if c1 < c2:
                        done = False
                        # Make new constraint
                        new_constraint = constraints[c2] - constraints[c1]
                        constraints[c2-c1] = new_constraint
                        for square in new_constraint:
                            squares_to_constraints[square].add(constraint)
                        # remove c2 constraint
                        for square in c2:
                            squares_to_constraints[square].remove(c2)
                        del constraints[c2]

                squares_to_constraints[square].add(constraint)
            new_constraints = {}

            # We remove constraints from the constraints dict, modify them and add
            # to the new constraints dict
            while constraints:

                # Pop an arbitrary constraint to analyze
                constraint, mines = constraints.popitem()
                # If one constraint is a subset of another, we can subtract to
                # simplify.
                subconstraint = None
                subconstraint_mines = None
                superconstraint = None
                superconstraint_mines = None
                for constraint2 in list(constraints):
                    if constraint <= constraint2:  # Tests subset
                        superconstraint = constraint2
                        superconstraint_mines = constraints[constraint2]
                        subconstraint = constraint
                        subconstraint_mines = mines
                        del constraints[constraint2]
                        break
                    elif constraint >= constraint2:
                        subconstraint = constraint2
                        subconstraint_mines = constraints[constraint2]
                        superconstraint = constraint
                        superconstraint_mines = mines
                        del constraints[constraint2]
                        break

                # If we found a superconstraint, remove both from the old list and
                # add modified one to new_constraints
                if superconstraint:
                    new_constraints[superconstraint - subconstraint] = (
                        superconstraint_mines - subconstraint_mines
                    )
                    new_constraints[subconstraint] = subconstraint_mines
                    done = False

                # If the constraint is at capacity or at empty, we can split into
                # individiual cells to simplify. Except if its already size 1.
                # Check if constraint is empty
                elif mines == 0 and len(constraint) > 1:
                    for coords in constraint:
                        new_constraints[frozenset([coords])] = 0
                    done = False
                elif mines == len(constraint) and len(constraint) > 1:
                    for coords in constraint:
                        new_constraints[frozenset([coords])] = 1
                    done = False
                else:
                    # If there is nothing to be done with this, just put it in the
                    # new list and don't reset the doneness tracker
                    new_constraints[constraint] = mines
            # At this point all constraints from the old list are gone
            constraints = new_constraints
            # print(constraints)

        # At this point, we are done making simplifications

        return constraints

    def __str__(self, constraints):
        out = ""

        for i, row in enumerate(self):
            current_string = ""
            for j, cell in enumerate(row):
                if cell is not None:
                    current_string += str(cell) + " "
                elif frozenset([(i, j)]) in constraints:
                    if constraints[frozenset([(i, j)])] == 0:
                        current_string += "  "
                    elif constraints[frozenset([(i, j)])] == 1:
                        current_string += "x "
                    else:
                        raise ValueError
                else:
                    current_string += "? "
            out += (current_string) + "\n"


TESTBOARD1 = MinesweeperBoard([[N, 2, 1, 1], [N, 3, N, 2], [1, 2, N, 2]])

print(TESTBOARD1, get_probabilities(TESTBOARD1))


TESTBOARD2 = [[1, 2, 1, 1], [N, N, N, 2], [N, N, N, 2]]

pretty_print_board(TESTBOARD2, get_probabilities(TESTBOARD2))
