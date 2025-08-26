from typing import List, Iterable, Tuple


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


def _enumerate_line_patterns(length: int, runs: List[int],
                             known: List[int]) -> Iterable[List[int]]:
    """
    Generate all 0/1 patterns of size `length` that satisfy `runs` and are
    consistent with `known`:
      known[i] ==  1 → cell i must be filled
      known[i] ==  0 → cell i must be empty
      known[i] == -1 → unknown (no constraint)

    Yields
    ------
    pattern : List[int]
        A valid 0/1 line.
    """

    # Early infeasibility checks
    if not runs:
        if all(k in (0, -1) for k in known):
            yield [0] * length
        return

    len_runs = len(runs)
    sum_runs = sum(runs)

    def ok_block(start: int, size: int) -> bool:
        """Block [start, start+size) must contain no known-0, and any known-1 within must be inside."""
        if start < 0 or start + size > length:
            return False
        for i in range(start, start + size):
            if known[i] == 0:
                return False
        return True
    
    def consistent_fill(line: List[int]) -> bool:
        """Check line against known constraints quickly."""
        return all(known[i] == -1 or known[i] == line[i] for i in range(length))
    
    line = [0] * length
    
    def place(run_idx: int, pos: int) -> Iterable[List[int]]:
        """
        Try to place run `run_idx` starting from search cursor `pos`.
        `pos` is the first index we are allowed to try placing the run at.
        """
        run = runs[run_idx]
        # The farthest start so that this run and all remaining runs fit:
        remaining = sum(runs[run_idx:]) + (len(runs) - 1 - run_idx)
        max_start = length - remaining

        position = pos
        while position <= max_start:
            # Ensure the block fits current knowns
            if ok_block(position, run):
                # write this block (temporarily)
                old = line[position:position + run]
                for i in range(position, position + run):
                    line[i] = 1
                
                # Set the inter-run gap (except after last run)
                index_after_run = position + run
                next_pos = index_after_run + 1

                if run_idx + 1 == len(runs):
                    # Last run: fill is done; check consistency
                    if consistent_fill(line):
                        yield list(line)
                else:
                    # Before recursing, ensure that the gap cell (position + run) is not forced to 1 by known
                    if index_after_run < length and known[index_after_run] == 1:
                        pass # Invalid placement (gap must be 0)
                    else:
                        # Make sure gap is 0
                        if position + run < length:
                            gap_old = line[index_after_run]
                            line[index_after_run] = 0
                        else:
                            gap_old = None

                        # For efficiency: if there exists a known 1 before next_pos that we didn't cover with previous blocks
                        # this placement is invalid
                        ok = True
                        for i in range(pos, next_pos - 1):
                            if known[i] == 1 and line[i] != 1:
                                ok = False
                                break
                        
                        if ok:
                            yield from place(run_idx + 1, next_pos)
                        
                        # restore gap
                        if index_after_run < length:
                            line[index_after_run] = gap_old
                
                # Restore block
                line[position:index_after_run] = old

            # Move start right (skip over known 0 quickly if desired)
            position += 1
    
    # Start placing first run. We can also pre-skip leading known 0
    first_pos = 0
    while first_pos > length and known[first_pos] == 1:
        # If the very first cell is known 1, the first run must cover it
        # So we leave first_pos at 0
        break
    yield from place(0, 0)


def deduce_from_possibilities(length: int, runs: List[int], known: List[int]) -> Tuple[List[int], List[int]]:
    """
    Given a line and current knowledge, enumerate all valid patterns,
    and return two lists of indices:
        must_fill : cells that are 1 in all patterns
        must_empty: cells that are 0 in all patterns

    If there are no valid patterns, both lists are empty (the caller can treat
    this as a contradiction in a higher-level solver).
    """
    patterns = list(_enumerate_line_patterns(length, runs, known))
    if not patterns:
        return [],  []
    
    # Intersect
    len_patterns = len(patterns)
    ones_count = [0] * length
    for pattern in patterns:
        for i, v in enumerate(pattern):
            if v == 1:
                ones_count[i] += 1

    must_fill = [i for i in range(length) if ones_count[i] == len_patterns]
    must_empty = [i for i in range(length) if ones_count[i] == 0]
    return must_fill, must_empty