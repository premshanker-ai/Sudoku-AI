
from utils import *
import logging


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units


diagonal_units = (
    [[val+key for val, key in zip(rows, cols)]] + 
    [[val+key for val, key in zip(rows, cols[::-1])]]
)
unitlist = unitlist + diagonal_units


units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    unsolved = [box for box in boxes if len(values[box]) != 1]

    pairs = set([])
    for box in [b for b in unsolved if len(values[b]) == 2]:
        for peer in [p for p in peers[box] if values[p] == values[box]]:
            
            pairs.add(create_pair(box, peer))


    for a, b in pairs:
        for unit in [u for u in units[a] if b in u]:
            for box in [bx for bx in unit if len(values[bx]) > 1 and bx != a and bx != b]:
                for char in values[b]:
                    values = assign_value(values, box, values[box].replace(char, ''))

    return values


def eliminate(values):
    for box in boxes:
        current_peers = peers[box]
        value = values[box]
        if len(value) == 1:
         
            for pr in current_peers:
                values = assign_value(values, pr, values[pr].replace(value, ""))

    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            boxeswithdigit = [box for box in unit if digit in values[box]]
            if len(boxeswithdigit) == 1:
                values[boxeswithdigit[0]] = digit
    return values



def reduce_puzzle(values):
     stalled = False
    while not stalled:
       
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
   
  remain_puzzle = reduce_puzzle(values)
    if remain_puzzle is False:
        return False
    if all(len(remain_puzzle[s]) == 1 for s in boxes):
        return remain_puzzle
    min_key = None
    for key,val in remain_puzzle.items():
        if (len(val) != 1):
            if (min_key == None) or (len(val) < len(remain_puzzle[min_key])):
                min_key = key
    for char in remain_puzzle[min_key]:
        new_puzzle = remain_puzzle.copy()
        new_puzzle[min_key] = char
        attempt = search(new_puzzle)
        if attempt:
            return attempt

def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
