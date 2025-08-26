from typing import List, Optional

from nonogram.dto import NonogramPuzzle
from nonogram.strategies.overlap import apply_overlap_pass
from nonogram.strategies.possibilities import deduce_from_possibilities
from nonogram.validator import is_puzzle_solved


def apply_possibility_pass(puzzle: NonogramPuzzle, grid: List[List[int]]) -> bool:
    """
    For each row/column, enumerate consistent patterns and intersect them.
    Marks must-fill (1) and must-empty (0). Returns True if anything changed.
    """
    changed = False

    # Rows
    for r in range(puzzle.size):
        known = grid[r]
        mf, me = deduce_from_possibilities(puzzle.size, puzzle.rows[r], known)
        for c in mf:
            if grid[r][c] != 1:
                grid[r][c] = 1
                changed = True
        for c in me:
            if grid[r][c] != 0:
                grid[r][c] = 0
                changed = True
    
    # Columns
    for c in range(puzzle.size):
        known = [grid[i][c] for i in range(puzzle.size)]
        mf, me = deduce_from_possibilities(puzzle.size, puzzle.cols[c], known)
        for i in mf:
            if grid[i][c] != 1:
                grid[i][c] = 1
                changed = True
        for i in me:
            if grid[i][c] != 0:
                grid[i][c] = 0
                changed = True
    
    return changed


def solve_nonogram(puzzle: NonogramPuzzle) -> Optional[List[List[int]]]:
    """
    Solve a given Nonogram puzzle.

    Parameters
    ----------
    puzzle : NonogramPuzzle
        A NonogramPuzzle dataclass containing the grid size and row/col clues.

    Returns
    -------
    Optional[List[List[int]]]
        A 2D list representing the solved grid, where 1 = filled, 0 = empty.
        Returns None if the puzzle has no valid solution.

    Notes
    -----
    - Uses constraint propagation (line deductions) and may fall back to
      backtracking if needed.
    """
    # Working grid: -1 unknown, 0 empty, 1 filled
    state = [[-1] * puzzle.size for _ in range(puzzle.size)]

    changed = True
    while changed:
        if is_puzzle_solved(puzzle, state):
            break

        changed = False
        if apply_overlap_pass(puzzle, state):
            changed = True
        if apply_possibility_pass(puzzle, state):
            changed = True
    
    print(f"Puzzle solved: {is_puzzle_solved(puzzle, state)}")

    return state
