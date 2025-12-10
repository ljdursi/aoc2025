#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department (navigating mazes of rolls of paper)

"""
import argparse
from typing import TextIO


class Map:
    """
    Represents a 2D map of the printing department.

    Attributes:
        grid (list[list[str]]): 2D list representing the map layout.
        nrows (int): Number of rows in the grid.
        ncols (int): Number of columns in the grid.
        max_neighbours (int): Maximum number of neighbors for a roll to be accessible.
        neighbour_count (list[list[int]]): Count of neighboring rolls for each cell.
        accessible (list[list[bool]]): Whether each cell is currently accessible.
    """

    def __init__(self, lines: list[str], max_neighbours: int = 4):
        """
        Initialize the map from a list of strings.

        Args:
            lines: List of strings representing the map rows.
            max_neighbours: Maximum number of roll neighbors for accessibility (default: 4).
        """
        self.grid = [list(line.strip()) for line in lines]
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0]) if self.nrows > 0 else 0
        self.max_neighbours = max_neighbours

        self.neighbour_count = [[0 for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.accessible = [[False for _ in range(self.ncols)] for _ in range(self.nrows)]
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.neighbour_count[r][c] = self.n_neighbours(r, c, tile='@')
                if self.grid[r][c] == '@' and self.neighbour_count[r][c] < max_neighbours:
                    self.accessible[r][c] = True

    def __str__(self):
        """Return string representation of the map."""
        return '\n'.join(''.join(row) for row in self.grid)

    def _iterate_neighbors(self, row: int, col: int):
        """
        Generator that yields (r, c) coordinates of all 8 neighboring cells.

        Args:
            row: Row index of the center cell.
            col: Column index of the center cell.

        Yields:
            Tuple of (row, col) for each valid neighboring cell.
        """
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.nrows and 0 <= c < self.ncols:
                    yield (r, c)

    def n_neighbours(self, row: int, col: int, tile: str = '@') -> int:
        """
        Count the number of neighboring tiles of a specific type.

        Args:
            row: Row index of the tile.
            col: Column index of the tile.
            tile: The tile character to count among neighbors (default: '@').

        Returns:
            The count of neighboring tiles matching the specified type.
        """
        count = 0
        for r, c in self._iterate_neighbors(row, col):
            if self.grid[r][c] == tile:
                count += 1
        return count

    def accessible_cells(self) -> list[tuple[int, int]]:
        """
        Get a list of all currently accessible cells.

        Returns:
            A list of (row, col) tuples for all accessible cells.
        """
        accessible = []
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.accessible[row][col]:
                    accessible.append((row, col))

        return accessible

    def remove_roll(self, row: int, col: int) -> bool:
        """
        Remove a roll of paper at the specified location.

        Args:
            row: Row index of the roll to remove.
            col: Column index of the roll to remove.

        Returns:
            True if a roll was removed, False if the cell was already empty.
        """
        if self.grid[row][col] != '@':
            return False

        self.grid[row][col] = '.'
        self.accessible[row][col] = False

        # Update neighbor counts and accessibility for neighboring cells
        for r, c in self._iterate_neighbors(row, col):
            self.neighbour_count[r][c] -= 1
            if self.neighbour_count[r][c] < self.max_neighbours and self.grid[r][c] == '@':
                self.accessible[r][c] = True

        return True


def get_inputs(fileobj: TextIO) -> list[str]:
    """
    Read and parse map data from a 2D text file.

    Reads lines from the file, where each line contains a string of map
    cells, either '@' (roll of paper) or '.' (empty space).

    Empty lines are skipped.

    Args:
        fileobj: A file-like object (or any iterator of strings) containing
                 map data, one row per line.

    Returns:
        A list of strings representing the map rows.
    """
    lines = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        lines.append(line)

    return lines


def main():
    """Main entry point for the printing department maze solver."""
    parser = argparse.ArgumentParser(
        prog='04',
        description="Advent of Code 2025 - Day 4: Printing Department"
    )
    parser.add_argument("input_file", type=argparse.FileType('r'), help="Input file containing map.")
    args = parser.parse_args()

    input_lines = get_inputs(args.input_file)
    printing_map = Map(input_lines)

    print("Part 1")
    accessible = printing_map.accessible_cells()
    print(len(accessible))

    print("Part 2")
    n_removed = 0
    while accessible:
        for (r, c) in accessible:
            printing_map.remove_roll(r, c)
        n_removed += len(accessible)
        accessible = printing_map.accessible_cells()

    print(n_removed)

if __name__ == "__main__":
    main()