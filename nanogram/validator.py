from typing import List
from .dto import NonogramPuzzle


def _line_groups_of_ones(line: List[int]) -> List[int]:
    """
    Convert a 0/1 line with no unknowns (-1) into run lengths of consecutive 1s.
    Example: [0,1,1,0,1] -> [2,1]
    """
    groups = []
    run = 0
    for v in line:
        if v == 1:
            run += 1
        else:
            if run:
                groups.append(run)
                run = 0
    if run:
        groups.append(run)
    return groups


def is_line_fully_known(line: List[int]) -> bool:
    """True if the line has no unknowns (-1)."""
    return all(v in (0, 1) for v in line)


def does_line_satisfy_clues(line: List[int], runs: List[int]) -> bool:
    """
    True if (and only if) the line is fully known and its 1-groups equal runs.
    """
    if not is_line_fully_known(line):
        return False
    return _line_groups_of_ones(line) == runs


def is_grid_complete(state: List[List[int]]) -> bool:
    """No unknowns anywhere."""
    return all(is_line_fully_known(row) for row in state)


def validate_rows(puzzle: NonogramPuzzle, state: List[List[int]]) -> List[int]:
    """
    Returns list of row indices that FAIL their clues (only checks fully-known rows).
    Rows with unknowns are not counted as failures here.
    """
    bad = []
    for r, runs in enumerate(puzzle.rows):
        row = state[r]
        if is_line_fully_known(row) and not does_line_satisfy_clues(row, runs):
            bad.append(r)
    return bad


def validate_cols(puzzle: NonogramPuzzle, state: List[List[int]]) -> List[int]:
    """
    Returns list of column indices that FAIL their clues (only checks fully-known cols).
    Columns with unknowns are not counted as failures here.
    """
    bad = []
    for c, runs in enumerate(puzzle.cols):
        col = [state[r][c] for r in range(puzzle.size)]
        if is_line_fully_known(col) and not does_line_satisfy_clues(col, runs):
            bad.append(c)
    return bad


def is_puzzle_solved(puzzle: NonogramPuzzle, state: List[List[int]]) -> bool:
    """
    True iff:
      - the grid is complete (no -1), and
      - every row and column exactly matches its clues.
    """
    if not is_grid_complete(state):
        return False

    # All rows/cols are fully known
    for r, runs in enumerate(puzzle.rows):
        if not does_line_satisfy_clues(state[r], runs):
            return False
    
    for c, runs in enumerate(puzzle.cols):
        col = [state[r][c] for r in range(puzzle.size)]
        if not does_line_satisfy_clues(col, runs):
            return False
    
    return True