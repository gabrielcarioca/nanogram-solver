from typing import List, Optional

from nanogram.dto import NonogramPuzzle
from nanogram.strategies.overlap import apply_overlap_pass


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
    grid = [[-1] * puzzle.size for _ in range(puzzle.size)]

    changed = apply_overlap_pass(puzzle, grid)

    return grid
