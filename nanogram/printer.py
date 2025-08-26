from typing import List

def print_grid(grid: List[List[int]]) -> None:
    """
    Print the grid using:
      '█' = filled (1)
      '·' = unknown (-1)
      ' ' = empty (0)  # we won't set empties in this first pass
    """
    symbols = {1: "█", 0: " ", -1: "·"}
    for row in grid:
        print("".join(symbols.get(v, "?") for v in row))