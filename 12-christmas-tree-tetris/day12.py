#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 12: Christmas Tree Tetris

Solves polyomino packing problems using trivial case detection
and backtracking for edge cases.
"""
import argparse
import re
from typing import TextIO
from dataclasses import dataclass
from enum import Enum


class Orientation(Enum):
    """Rotation angles for shape orientation."""
    deg_0   = 0
    deg_90  = 1
    deg_180 = 2
    deg_270 = 3


@dataclass(frozen=True)
class Shape:
    """
    A polyomino shape that fits in a 3x3 bounding box.

    Attributes:
        grid: Set of (x, y) coordinates of filled cells
        shape: (width, height) of bounding box
    """
    grid: set[tuple[int,int]]
    shape: tuple[int, int]

    def __init__(self, points: list[tuple[int,int]]):
        xs, ys = zip(*points)
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        object.__setattr__(self, 'grid', set([(x - minx, y - miny) for x, y in points]))
        object.__setattr__(self, 'shape', (maxx - minx + 1, maxy - miny + 1))

    @classmethod
    def from_lines(cls, lines: list[str]) -> 'Shape':
        """Parse a shape from text lines where '#' indicates filled cells."""
        points: list[tuple[int, int]] = []
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == '#':
                    points.append((x, y))
        return Shape(points)

    @classmethod
    def _rotation_function(cls, o: Orientation):
        match o:
            case Orientation.deg_0: 
                return lambda x, y, maxx, maxy: (x, y)
            case Orientation.deg_90:
                return lambda x, y, maxx, maxy: (maxy - y, x)
            case Orientation.deg_180:
                return lambda x, y, maxx, maxy: (maxx - x, maxy - y)
            case Orientation.deg_270: 
                return lambda x, y, maxx, maxy: (y, maxx - x)

    def rotate(self, o: Orientation) -> 'Shape':
        maxx, maxy = self.shape
        rot = Shape._rotation_function(o)

        new_points: list[tuple[int, int]] = [rot(x, y, maxx, maxy) for x, y in self.grid]
        return Shape(new_points)

    def flip_horizontal(self) -> 'Shape':
        """Flip the shape horizontally."""
        maxx = self.shape[0] - 1
        new_points = [(maxx - x, y) for x, y in self.grid]
        return Shape(new_points)

    def all_orientations(self) -> list['Shape']:
        """
        Generate all unique orientations (rotations and flips).

        Returns list of unique shapes created by applying all rotations
        (0°, 90°, 180°, 270°) and horizontal flip. Duplicates are filtered.
        """
        orientations = []
        seen = set()

        # Try all rotations
        for orientation in Orientation:
            rotated = self.rotate(orientation)
            key = frozenset(rotated.grid)
            if key not in seen:
                seen.add(key)
                orientations.append(rotated)

        # Try all rotations of the flipped shape
        flipped = self.flip_horizontal()
        for orientation in Orientation:
            rotated = flipped.rotate(orientation)
            key = frozenset(rotated.grid)
            if key not in seen:
                seen.add(key)
                orientations.append(rotated)

        return orientations

    def __len__(self) -> int:
        return len(self.grid)

    def __str__(self):
        lines = [list("." * self.shape[0]) for _ in range(self.shape[1])]
        for x, y in self.grid:
            lines[y][x] = '#'

        return '\n'.join([''.join(line) for line in lines])


@dataclass(frozen=True)
class Requirements:
    """
    Packing requirements for a single problem instance.

    Attributes:
        size: (width, height) of grid to pack into
        counts: List of how many of each shape to pack
    """
    size: tuple[int, int]
    counts: list[int]

    @classmethod
    def from_str(cls, line: str) -> 'Requirements':
        sizestr, countsstr = line.split(':')
        sizes: list[int] = [int(s) for s in sizestr.split('x')]

        if len(sizes) != 2:
            raise ValueError(f"Invalid number of sizes for Requirement: {line}")

        counts: list[int] = [int(c) for c in countsstr.strip().split()]

        return Requirements(tuple(sizes), counts)

    def __str__(self) -> str:
        return f"{self.size[0]}x{self.size[1]}: " + " ".join([str(c) for c in self.counts])

    def area(self) -> int:
        return self.size[0] * self.size[1]


class Solver:
    """
    Backtracking solver for shape packing problems.

    Uses a simple recursive backtracking approach, filling the grid
    left-to-right, top-to-bottom. Only used for cases not handled by
    trivial detection (which is rare in practice).
    """

    def __init__(self, shapes: list[Shape], requirements: Requirements):
        self.shapes = shapes
        self.width, self.height = requirements.size
        self.counts = requirements.counts.copy()
        self.occupied: set[tuple[int, int]] = set()

        # Precompute all orientations for each shape
        self.all_orientations: list[list[Shape]] = []
        for shape in shapes:
            self.all_orientations.append(shape.all_orientations())

    def can_place(self, shape: Shape, x: int, y: int) -> bool:
        """Check if shape can be placed at position (x, y)."""
        for dx, dy in shape.grid:
            nx, ny = x + dx, y + dy
            # Check bounds
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                return False
            # Check collision
            if (nx, ny) in self.occupied:
                return False
        return True

    def place(self, shape: Shape, x: int, y: int) -> None:
        """Place shape at position (x, y)."""
        for dx, dy in shape.grid:
            self.occupied.add((x + dx, y + dy))

    def unplace(self, shape: Shape, x: int, y: int) -> None:
        """Remove shape from position (x, y)."""
        for dx, dy in shape.grid:
            self.occupied.remove((x + dx, y + dy))

    def find_first_empty(self) -> tuple[int, int] | None:
        """Find the first empty cell (scanning left-to-right, top-to-bottom)."""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.occupied:
                    return (x, y)
        return None

    def solve(self) -> bool:
        """Try to pack all shapes. Returns True if successful."""
        # Check if we're done
        if all(count == 0 for count in self.counts):
            return True

        # Quick fail: not enough space for remaining shapes
        remaining_cells = self.width * self.height - len(self.occupied)
        needed_cells = sum(count * len(self.shapes[i]) for i, count in enumerate(self.counts))
        if remaining_cells < needed_cells:
            return False

        # Find the first empty cell to maintain search ordering
        first_empty = self.find_first_empty()
        if first_empty is None:
            return False

        target_x, target_y = first_empty

        # Try each shape type with remaining count
        for shape_idx in range(len(self.shapes)):
            if self.counts[shape_idx] == 0:
                continue

            # Try all orientations
            for oriented_shape in self.all_orientations[shape_idx]:
                # Try all positions from first empty onwards
                for y in range(target_y, self.height):
                    start_x = target_x if y == target_y else 0
                    for x in range(start_x, self.width):
                        if self.can_place(oriented_shape, x, y):
                            self.place(oriented_shape, x, y)
                            self.counts[shape_idx] -= 1

                            if self.solve():
                                return True

                            self.counts[shape_idx] += 1
                            self.unplace(oriented_shape, x, y)

        return False


def can_pack_trivial(shapes: list[Shape], requirements: Requirements) -> bool | None:
    """
    Check if packing is trivially solvable or unsolvable.

    Returns:
        True if trivially solvable (enough 3x3 regions for all shapes)
        False if trivially unsolvable (too many cells needed)
        None if needs backtracking solver
    """
    counts = requirements.counts
    total_shapes = sum(counts)
    needed_cells = sum(count * len(shapes[i]) for i, count in enumerate(counts))

    # Trivial NO: need more cells than available
    if needed_cells > requirements.area():
        return False

    # Trivial YES: enough non-overlapping grid regions for all shapes
    if shapes:
        grid_size = max(shapes[0].shape)
        width, height = requirements.size
        max_regions = (width // grid_size) * (height // grid_size)

        if total_shapes <= max_regions:
            return True

    # Needs actual solving
    return None


def get_inputs(fileobj: TextIO) -> tuple[list[Shape], list[Requirements]]:
    """Parse input file containing shape definitions and packing requirements."""
    lines = [line.rstrip('\n') for line in fileobj.readlines()]
    shapes: list[Shape] = []
    requirements: list[Requirements] = []

    doing_shapes = True
    current_lines: list[str] = []

    for line in lines:
        if not doing_shapes:
            requirements.append(Requirements.from_str(line))
            continue

        if re.match(r"^\d+x\d+:", line):
            # Found a requirement line - save current shape and switch modes
            if current_lines:
                shapes.append(Shape.from_lines(current_lines))
            doing_shapes = False
            requirements.append(Requirements.from_str(line))
        elif re.match(r"^\d+:", line):
            # Found a shape header - save previous shape if any
            if current_lines:
                shapes.append(Shape.from_lines(current_lines))
            current_lines.clear()
        elif not line and current_lines:
            # Empty line - end of current shape
            shapes.append(Shape.from_lines(current_lines))
            current_lines.clear()
        else:
            # Shape data line
            current_lines.append(line)

    return shapes, requirements


def main() -> None:
    """Main entry point for the solution."""
    parser = argparse.ArgumentParser(
        prog='day12',
        description="Advent of Code 2025 - Day 12: Presents Under The Tree"
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType('r'),
        help="Input file containing shapes and requirements"
    )
    args = parser.parse_args()

    shapes, requirements = get_inputs(args.input_file)

    print("Part 1")
    solved_count = 0

    for req in requirements:
        trivial_result = can_pack_trivial(shapes, req)

        if trivial_result is True:
            solved_count += 1
        elif trivial_result is None:
            # Needs backtracking solver
            solver = Solver(shapes, req)
            if solver.solve():
                solved_count += 1
        # else: trivial_result is False, not solvable

    print(solved_count)

if __name__ == "__main__":
    main()
