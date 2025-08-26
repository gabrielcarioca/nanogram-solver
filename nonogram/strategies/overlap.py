""" This module handless the overlap pass for the nanogram puzzle """

from typing import List

from nonogram.dto import NonogramPuzzle


def overlap_fill_line(length: int, runs: List[int]) -> List[int]:
    """
    Compute the indices that are guaranteed filled for a single line using
    the classic "overlap/core fill" logic (ignores any prior cell knowledge).

    Parameters
    ----------
    length : int
        Number of cells in the line.
    runs : List[int]
        Ordered run lengths for the line. Example: [3,1].

    Returns
    -------
    List[int]
        Sorted unique indices (0-based) that must be filled.
        Empty if no overlap forces any cell.

    Notes
    -----
    Let L=length, k=len(runs), req=sum(runs)+(k-1), slack S=L-req.
    For each run i:
      earliest start  E[i]   = sum(runs[0..i-1]) + i
      latest start    Lmax[i]= L - ( sum(runs[i..k-1]) + (k-1 - i) )
      overlap length  OL[i]  = max(0, runs[i] - S)
      If OL[i] > 0, the forced block is the intersection region between
      the earliest end (E[i]+runs[i]-1) and the latest start (Lmax[i]),
      which yields the contiguous indices [Lmax[i], E[i]+runs[i]-1].
    """

    if not runs:
        return []
    
    k = len(runs)
    req = sum(runs) + (k - 1)
    S = length - req # slack
    if S < 0:
        # Impossible line
        return []

    # prefix sums of runs for fast range sums
    pref = [0] * (k + 1)
    for i in range(1, k + 1):
        pref[i] = pref[i - 1] + runs[i - 1]
    
    forced: List[int] = []

    for i in range(k):
        r = runs[i]
        overlap_len = r - S
        if overlap_len <= 0:
            continue # No overlap cells

        # Earliest start for run i (accounting for i gaps before it) - push everything as far left as possible
        earliest_start = pref[i] + i

        # Latest start for run i - push everythong as far right as possible
        # sum(runs[i...k-1]) = pref[k] - pref[i]
        # gaps after i = (k-1 - i)
        latest_start = length - ((pref[k] - pref[i]) + (k - 1 - i))

        # Run i can slide between earliesst_start and latest_start (The slack S)

        # Forced blocks runs from latest_start .. (earliest_start + r - 1)
        start = latest_start
        end = earliest_start + r - 1

        if start <= end:
            forced.extend(range(start, end + 1))
    

    return sorted(set(forced))


def apply_overlap_pass(puzzle: NonogramPuzzle, grid: List[List[int]]) -> bool:
    """
    Apply one global "overlap/core fill" pass to all rows and columns.
    Only marks cells as filled (1) when forced by overlap; does NOT mark empties.

    Parameters
    ----------
    puzzle : NonogramPuzzle
        The puzzle definition.
    grid : List[List[int]]
        Mutable working grid: -1 unknown, 0 empty, 1 filled.

    Returns
    -------
    bool
        True if the grid was changed (some new cells filled), False otherwise.

    Mapping
    -------
    - Rows: left → right index mapping is (row=r, col=c).
    - Cols: top → bottom index mapping is (row=i, col=c) for index i in that column.
    """
    changed = False
    N = puzzle.size

    # Rows
    for r in range(N):
        forced = overlap_fill_line(N, puzzle.rows[r])
        for c in forced:
            if grid[r][c] == -1:
                grid[r][c] = 1
                changed = True
    
    # Columns
    for c in range(N):
        forced = overlap_fill_line(N, puzzle.cols[c])
        for i in forced:
            if grid[i][c] == -1:
                grid[i][c] = 1
                changed = True
    
    return changed