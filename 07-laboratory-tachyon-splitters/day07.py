#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 7: Tachyon Splitting in the Laboratory

"""
import argparse
from typing import TextIO
from enum import Enum
from collections import namedtuple, defaultdict

Point = namedtuple("Point", ["row", "col"])
Path = namedtuple("Path", ["start", "end"])

class MapCell(Enum):
    SOURCE = 'S'
    EMPTY = '.'
    SPLITTER = '^'

    @classmethod
    def from_str(cls, s: str) -> "MapCell":
        for cell in cls:
            if cell.value == s:
                return cell
        raise ValueError(f"Invalid cell string: {s}")

    def to_str(self) -> str:
        return self.value


class Map:
    """
    Represents a 2D map of the tachyon laboratory.

    Attributes:
        nrows (int): Number of rows in the map.
        ncols (int): Number of columns in the map.
        map (dict[Point, MapCell]): Mapping of positions to cell types.
        splitters_by_col (dict[int, list[int]]): Splitter rows indexed by column for fast lookup.
        sources (list[Point]): List of tachyon source positions.
    """

    def __init__(self, lines: list[str]):
        """
        Initialize the map from a list of strings.

        Args:
            lines: List of strings representing the map rows.
        """
        self.nrows = len(lines)
        self.ncols = len(lines[0].strip()) if self.nrows > 0 else 0
        self.map: dict[Point, MapCell] = {}
        self.splitters_by_col: dict[int, list[int]] = {}
        self.sources: list[Point] = []

        for row, line in enumerate(lines):
            for col, char in enumerate(line.strip()):
                if char == MapCell.SOURCE.value:
                    self.sources.append(Point(row, col))
                    self.map[Point(row, col)] = MapCell.SOURCE
                elif char == MapCell.SPLITTER.value:
                    if col not in self.splitters_by_col:
                        self.splitters_by_col[col] = [row]
                    else:
                        self.splitters_by_col[col].append(row)
                    self.map[Point(row, col)] = MapCell.SPLITTER

        for col in self.splitters_by_col:
            self.splitters_by_col[col].sort()

    def __getitem__(self, key: Point) -> MapCell:
        r, c = key
        if key in self.sources:
            return MapCell.SOURCE
        elif c in self.splitters_by_col and r in self.splitters_by_col[c]:
            return MapCell.SPLITTER
        else:
            return MapCell.EMPTY

    def __str__(self):
        """Return string representation of the map."""
        return '\n'.join(''.join(self.__getitem__((r, c)).to_str() for c in range(self.ncols)) for r in range(self.nrows))

    def __splitters_past_row_in_col(self, row: int, col: int) -> list[int]:
        if col not in self.splitters_by_col:
            return []
        return [r for r in self.splitters_by_col[col] if r > row]

    def propagate(self, source: Point = None) -> tuple[set[Point], list[Path]]:
        """
        Propagate tachyon rays from the given source (or the first source if None).

        Args:
            source: Starting point for beam propagation (defaults to first source in map)

        Returns:
            Tuple of (splitters_hit, paths) where:
                - splitters_hit: Set of Points where splitters were encountered
                - paths: List of Path objects representing beam segments
        """
        if source is None:
            if not self.sources:
                raise ValueError("No sources defined in the map")
            source = self.sources[0]
            if len(self.sources) > 1:
                raise ValueError("Multiple sources defined - not implemented")

        splitters_hit: set[Point] = set()
        paths: set[Path] = set()

        active_rays: list[Point] = [source]
        while active_rays:
            current = active_rays.pop()
            r, c = current

            # Skip if already off the map (bottom, left, or right)
            if r >= self.nrows or c < 0 or c >= self.ncols:
                continue

            splitters = self.__splitters_past_row_in_col(r, c)
            if not splitters:
                # No splitters in this column, ray exits the map
                paths.add(Path(current, Point(self.nrows, c)))
                continue

            splitter_row = splitters[0]
            splitter_pos = Point(splitter_row, c)
            paths.add(Path(current, splitter_pos))

            if splitter_pos in splitters_hit:
                # This splitter has already been hit, ray is absorbed
                continue

            splitters_hit.add(splitter_pos)

            # Create two new beams going left and right
            left_pos = Point(splitter_row + 1, c - 1)
            right_pos = Point(splitter_row + 1, c + 1)
            paths.add(Path(splitter_pos, left_pos))
            paths.add(Path(splitter_pos, right_pos))

            active_rays.append(left_pos)
            active_rays.append(right_pos)

        return splitters_hit, sorted(list(paths), key=lambda x: x.start.row)


def get_inputs(fileobj: TextIO) -> Map:
    """
    Parse input file containing a laboratory map.

    Args:
        fileobj: Text file object to read from

    Returns:
        A Map object representing the laboratory layout
    """
    lines = [line.rstrip('\n') for line in fileobj.readlines() if line.strip()]
    return Map(lines)


def count_paths_to_exit(lab_map: Map, paths: list[Path]) -> int:
    """
    Count the total number of distinct paths from source to map exit.

    This function traces through all beam paths and counts how many distinct
    ways a beam can travel from the source to exiting the map. When beams
    split at splitters, both branches are counted as separate paths.

    Since beams always move downward, we can process points in row order
    (a natural topological ordering) rather than using Kahn's algorithm.

    Args:
        lab_map: The Map object containing the laboratory layout
        paths: List of Path objects representing beam segments from propagate()

    Returns:
        Total number of distinct paths from source to exit
    """
    if not lab_map.sources:
        return 0

    # Build adjacency list mapping each point to its successors
    outgoing: dict[Point, list[Point]] = defaultdict(list)
    all_nodes = {lab_map.sources[0]}

    for p in paths:
        outgoing[p.start].append(p.end)
        all_nodes.add(p.start)
        all_nodes.add(p.end)

    # Since beams always move downward, we can process points in row order
    # This gives us a natural topological ordering without needing Kahn's algorithm
    sorted_nodes = sorted(all_nodes, key=lambda p: (p.row, p.col))

    # Count paths to each node
    npaths: dict[Point, int] = {lab_map.sources[0]: 1}

    for current in sorted_nodes:
        if current not in npaths:
            # This node is not reachable from the source
            continue

        # Propagate path count to all successors
        for next_node in outgoing[current]:
            if next_node not in npaths:
                npaths[next_node] = 0
            npaths[next_node] += npaths[current]

    # Count paths that exit the map by finding unique exit points
    # Beams can exit from bottom (row == nrows), left (col < 0), or right (col >= ncols)
    exit_points = {
        p.end for p in paths
        if p.end.row >= lab_map.nrows or p.end.col < 0 or p.end.col >= lab_map.ncols
    }
    total_paths = sum(npaths.get(point, 0) for point in exit_points)

    return total_paths


def main():
    """Main entry point for the laboratory tachyon splitter solver."""
    parser = argparse.ArgumentParser(
        prog='07',
        description="Advent of Code 2025 - Day 7: Tachyon Splitting in the Laboratory"
    )
    parser.add_argument("input_file", type=argparse.FileType('r'), help="Input file containing laboratory map.")
    args = parser.parse_args()

    lab_map = get_inputs(args.input_file)
    print(lab_map)

    splitters_hit, paths = lab_map.propagate()

    print("Part 1")
    print(len(splitters_hit))

    print("Part 2")
    total_paths = count_paths_to_exit(lab_map, paths)
    print(total_paths)

if __name__ == "__main__":
    main()