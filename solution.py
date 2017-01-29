assignments = []

# to be used to define the naming of the sudoku i.e. boxes
rows = 'ABCDEFGHI'
cols = '123456789'
all_digits = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    pass
    return [s + t for s in A for t in B]

# Creating the keys for all the boxes
boxes = cross(rows, cols)

# Creating units where each one of them follow the sudoku constraint
# Row units
row_units = [cross(r, cols) for r in rows]

# all the column units
column_units = [cross(rows, c) for c in cols]

# all the 3x3 squares
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# additional diagonal units
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                  ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]

# all the units together so that we can iterate each one them while using the constraint propagation to reduce the search space
unitlist = row_units + column_units + square_units + diagonal_units

# dictonary of boxes and its units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# dictonary of boxes and its peers
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # For each unit in the all units(constraints)
    for unit in unitlist:
        # find the boxes which have search space of length two
        key_length_2 = [box for box in unit if len(values[box]) == 2]
        two_dict = dict(zip(key_length_2, [values[key] for key in key_length_2]))

        # find the naked twins and their keys. To do so reverse the dictonary and find keys of length 2 in this new dictionary
        rev_multidict = {}
        for key, value in two_dict.items():
            rev_multidict.setdefault(value, set()).add(key)

        naked_twin = ([key for key, values in rev_multidict.items() if len(values) == 2])

        # If there is a naked twin in this unit
        if len(naked_twin) > 0:
            # get the keys with this naked twin
            naked_twin_keys = rev_multidict[naked_twin[0]]

            # remove naked twin from search space of all other boxes in this unit
            for box in unit:
                # make sure that we are not removing the search space of the naked twin boxes
                if box not in naked_twin_keys:
                    # reduce the seach space
                    for digit in naked_twin[0]:
                        values[box] = values[box].replace(digit, "")

    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []

    for c in grid:
        if c in all_digits:
            chars.append(c)
        if c == '.':
            chars.append(all_digits)
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    new_values = values.copy()  # note: do not modify original values
    # TODO: Implement only choice strategy here
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                new_values[dplaces[0]] = digit
    return new_values


def reduce_puzzle(values):

    # reduces the search space iteratively by applying each technique one by one (constraint propagation)
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked twin strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
