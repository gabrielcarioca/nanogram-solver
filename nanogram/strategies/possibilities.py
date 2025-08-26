from typing import List

def generate_line_possibilities(
    length: int,
    runs: List[int],
    known_filled_mask: int = 0,
    known_empty_mask: int = 0,
) -> List[int]:
    """
    Enumerate all legal fillings (as bitmasks) for a single Nonogram line.

    A "line" is either a row (evaluated left → right) or a column (top → bottom).
    The function returns every pattern that satisfies the run-length clues and
    is consistent with any already-fixed cells.

    Parameters
    ----------
    length : int
        Number of cells in the line.
    runs : List[int]
        Ordered run lengths for the line. Example: [3, 1] means a block of 3
        filled cells, at least one empty cell, then a block of 1 filled cell.
        An empty list [] represents a fully empty line.
    known_filled_mask : int, optional
        Bitmask of cells already known to be filled (1-bits = must be filled).
        Bit index 0 corresponds to the leftmost (or topmost) cell; bit i to cell i.
        Default is 0 (no prior knowledge).
    known_empty_mask : int, optional
        Bitmask of cells already known to be empty (1-bits = must be empty).
        Must be disjoint from `known_filled_mask`. Default is 0.

    Returns
    -------
    List[int]
        A list of bitmasks, each mask representing one valid pattern of filled
        cells for the line. For a returned mask `m`, bit i = 1 means cell i is
        filled; bit i = 0 means cell i is empty.

    Behavior & Constraints
    ----------------------
    - Patterns must place the runs in order, with at least one empty cell
      separating adjacent runs (no separator required before the first or after
      the last run).
    - Every returned pattern `m` must satisfy:
        * `(m & known_empty_mask) == 0` (never fill a known empty cell)
        * `(known_filled_mask & ~m) == 0` (never leave a known filled cell empty)
    - If `runs` is empty, the only legal pattern is the all-empty mask,
      provided it does not conflict with `known_filled_mask`.

    Notes
    -----
    - This function is purely combinational (no mutation). It is suitable for
      caching/memoization keyed by `(length, tuple(runs), known_filled_mask, known_empty_mask)`.
    - Typical implementation uses recursive/backtracking placement or dynamic
      programming to place runs and generate masks efficiently.
    - If no legal pattern exists, returns an empty list.

    Examples
    --------
    >>> # length = 5, runs = [2], no prior knowledge
    >>> generate_line_possibilities(5, [2], 0, 0)
    [... bitmasks representing: 11000, 01100, 00110, 00011 ...]

    >>> # same line, but cell 0 known empty (bit 0 set in known_empty_mask)
    >>> generate_line_possibilities(5, [2], 0, 0b00001)
    [... masks representing: 01100, 00110, 00011 ...]

    >>> # contradiction example: cell 0 known filled, runs=[]
    >>> generate_line_possibilities(5, [], 0b00001, 0)
    []
    """
    pass
