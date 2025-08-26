from dataclasses import dataclass
from typing import List


@dataclass
class NonogramPuzzle:
    """
    Data representation of a Nonogram puzzle.

    Attributes
    ----------
    size : int
        Size of the puzzle grid (assumed square: size x size).
    rows : List[List[int]]
        Row clues. Each entry is a list of run lengths (left → right).
    cols : List[List[int]]
        Column clues. Each entry is a list of run lengths (top → bottom).
    """
    size: int
    rows: List[List[int]]
    cols: List[List[int]]
