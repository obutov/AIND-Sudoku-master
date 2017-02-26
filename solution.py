import sys

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows[::-1], cols)]]
unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

assignments = []


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
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Iterate over each available unit and search for twins
    for unit in unit_list:
        # get any possible twin values for the unit
        # and eliminate these values in the unit's boxes
        for twin_value in get_unit_twin_values(values, unit):
            # Eliminate the naked twins as possibilities for their peers
            values = eliminate_values_from_unit_boxes(values, unit, twin_value)

    return values


def get_unit_twin_values(values, unit):
    """
    Get twin values for the unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        unit(list): a list of unit boxes (A1, A2, A3, ...)
    Returns:
        the list of twins' values (23, 56, ...)
    """
    # get twin candidate, e.g. any boxes with values' strings of length = 2
    twin_candidates = [(values[box], box) for box in unit if len(values[box]) == 2]

    # count boxes' value occurrences in the unit
    twin_candidates_counts = {}
    for v, b in twin_candidates:
        twin_candidates_counts[v] = twin_candidates_counts.get(v, 0) + 1

    # Get twins' values from the counts list where counts = 2, e.g. box is repeated exactly twice
    twins = [key for key, value in twin_candidates_counts.items() if value == 2]
    # Return unique values
    return [twin_value for twin_value in list(set(twins))]


def eliminate_values_from_unit_boxes(values, unit, strip_values):
    """
    Strips the values from the unit boxes
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        unit(list): a list of unit boxes (A1, A2, A3, ...)
        strip_values(string): values to be stripped from the the unit boxes
    Returns:
        the values dictionary with the naked twins eliminated
    """
    for box in unit:
        changing_value = values[box]
        eliminated = False
        # prevent eliminating twins themselves
        if changing_value != strip_values:
            # iterate over strip values, digit by digit
            for remove_letter in strip_values:
                # only attempt to strip the digit, if it is present in the box
                if remove_letter in changing_value:
                    changing_value = changing_value.replace(remove_letter, '')
                    eliminated = True
            if eliminated:
                # assign new value whenever digits are eliminated
                values = assign_value(values, box, changing_value)
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
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
     Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
     Args:
         values(dict): The sudoku in dictionary form
     Returns:
         The resulting sudoku in dictionary form.
     """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        values(dict): Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    Execute Sudoku solving strategies to reduze puzzle
    Args:
        values(dict): Sudoku in dictionary form.
    Returns:
        Solved puzzle or False whenever Sudoku cannot be solved (i.e. stalled)
    """
    stalled = False
    solved = False
    while not stalled and not solved:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)

        # Only Choice Strategy
        values = only_choice(values)

        # Naked Twin Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        solved = solved_values_after == 81
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Using depth-first search and propagation, try all possible values."
    Args:
        values(dict): Sudoku in dictionary form.
    Returns:
        Solved puzzle or False
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
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
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.', exc_type, exc_value, exc_traceback)
