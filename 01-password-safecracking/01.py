#!/usr/bin/env python3
"""
Safe Cracking Puzzle Solver

This module solves a puzzle involving a safe with a rotary dial. The dial has
positions numbered 0-99 and can be rotated left or right. The solution tracks:
  - The final position after each rotation
  - How many times the dial passes through position 0 during rotations

Part 1: Count how many times the dial lands on position 0
Part 2: Count total times dial points at 0 (landings + crossings during rotation)
"""
import argparse
import sys
from enum import Enum
from typing import TextIO


class RotDir(Enum):
    """
    Enumeration for rotation direction on a dial.

    LEFT represents counter-clockwise rotation (decreasing position numbers).
    RIGHT represents clockwise rotation (increasing position numbers).
    """
    LEFT = -1
    RIGHT = 1

class Rotation(object):
    """
    Represents a single rotation instruction for the safe dial.

    Attributes:
        direction (RotDir): The direction to rotate (LEFT or RIGHT).
        steps (int): The number of positions to rotate.
    """

    def __init__(self, direction: RotDir, steps: int):
        """
        Initialize a rotation instruction.

        Args:
            direction: The direction to rotate (RotDir.LEFT or RotDir.RIGHT).
            steps: The number of positions to rotate.
        """
        self.direction = direction
        self.steps = steps

    def __str__(self):
        """Return string representation in format 'L68' or 'R48'."""
        dir_char = 'L' if self.direction == RotDir.LEFT else 'R'
        return f"{dir_char}{self.steps}"

class SafeState(object):
    """
    Tracks the state of a safe's rotary dial through a series of rotations.

    The dial has positions numbered 0 to dial_size-1. Rotations wrap around, and
    the state tracks both the current position and how many times the dial has
    passed through position 0 during rotations (not counting ending positions).

    Attributes:
        dial_size (int): The number of positions on the dial (default 100).
        current_position (int): The current position of the dial (0 to dial_size-1).
        zero_crossings (int): Count of times dial passed through 0 during rotations.
    """

    def __init__(self, dial_size: int=100, current_position: int = 0):
        """
        Initialize the safe state.

        Args:
            dial_size: The number of positions on the dial (default 100).
            current_position: The starting position of the dial (default 0).
        """
        self.dial_size = dial_size
        self.current_position = current_position % dial_size
        self.zero_crossings = 0

    def _count_multiples_between(self, start: int, end: int, multiple: int) -> int:
        """
        Count how many multiples of 'multiple' exist strictly between start and end.

        This is used to count how many times the dial crosses position 0 (or any
        other multiple of dial_size) during a rotation. The count excludes the
        start and end positions themselves.

        Args:
            start: The starting position (unwrapped, can be negative or > dial_size).
            end: The ending position (unwrapped, can be negative or > dial_size).
            multiple: The multiple to count (typically dial_size for zero crossings).

        Returns:
            The number of multiples strictly between start and end.

        Example:
            _count_multiples_between(50, 150, 100) returns 1 (crosses 100 once)
            _count_multiples_between(50, 250, 100) returns 2 (crosses 100 and 200)
        """
        min_pos, max_pos = min(start, end), max(start, end)
        first = (min_pos // multiple + 1) * multiple
        last = max_pos // multiple * multiple
        if max_pos % multiple == 0:
            last -= multiple
        return max(0, (last - first) // multiple + 1)

    def rotate(self, rotation: Rotation):
        """
        Apply a rotation to the dial and update state.

        This method:
        1. Calculates the new position after the rotation
        2. Counts how many times the rotation crosses position 0
        3. Updates the current position (with wrapping)
        4. Increments the zero_crossings counter

        Args:
            rotation: The rotation instruction to apply.

        Example:
            Starting at position 50, rotating L68 moves to position 82 and
            crosses 0 once (going 50 -> 0 -> 82 in the counter-clockwise direction).
        """
        start = self.current_position
        end = start + (rotation.steps if rotation.direction == RotDir.RIGHT else -rotation.steps)

        self.zero_crossings += self._count_multiples_between(start, end, self.dial_size)
        self.current_position = end % self.dial_size

    def get_position(self) -> int:
        """
        Get the current position of the dial.

        Returns:
            The current position (0 to dial_size-1).
        """
        return self.current_position

    def get_zero_crossings(self) -> int:
        """
        Get the count of zero crossings during rotations.

        This counts how many times the dial passed through position 0 during
        rotations, NOT including times when rotations ended at position 0.

        Returns:
            The number of zero crossings during rotations.
        """
        return self.zero_crossings

    def apply_rotations(self, rotations: list[Rotation]) -> list[int]:
        """
        Apply a sequence of rotations and return all ending positions.

        Args:
            rotations: A list of Rotation objects to apply in sequence.

        Returns:
            A list of positions after each rotation. The list length equals
            the number of rotations.

        Example:
            Starting at 50, applying [L68, L30] returns [82, 52].
        """
        positions = []
        for rotation in rotations:
            self.rotate(rotation)
            positions.append(self.get_position())

        return positions

def parse_rotation_line(line: str) -> Rotation:
    """
    Parse a single line into a Rotation object.

    The line should be in the format 'L<number>' or 'R<number>' where L indicates
    a left (counter-clockwise) rotation and R indicates a right (clockwise) rotation.

    Args:
        line: A string like 'L68' or 'R48'. Leading/trailing whitespace is ignored.

    Returns:
        A Rotation object with the parsed direction and steps.

    Raises:
        ValueError: If the line is empty, has an invalid direction character,
                   or the number cannot be parsed as an integer.

    Examples:
        parse_rotation_line("L68") -> Rotation(RotDir.LEFT, 68)
        parse_rotation_line("R48") -> Rotation(RotDir.RIGHT, 48)
        parse_rotation_line("  L30  ") -> Rotation(RotDir.LEFT, 30)
    """
    line = line.strip()
    if not line:
        raise ValueError("Empty line cannot be parsed as rotation")

    direction_char = line[0]
    steps = int(line[1:])

    if direction_char == 'L':
        direction = RotDir.LEFT
    elif direction_char == 'R':
        direction = RotDir.RIGHT
    else:
        raise ValueError(f"Invalid direction character: {direction_char}")

    return Rotation(direction, steps)


def get_inputs(fileobj: TextIO) -> list[Rotation]:
    """
    Read and parse rotation instructions from a file-like object.

    Reads lines from the file, where each line should be in the format 'L<number>'
    or 'R<number>'. Empty lines are skipped.

    Args:
        fileobj: A file-like object (or any iterator of strings) containing
                rotation instructions, one per line.

    Returns:
        A list of Rotation objects parsed from the non-empty lines.

    Example:
        If the file contains:
            L68
            L30

            R48
        This function returns a list of 3 Rotation objects.
    """
    rotations = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue
        rotations.append(parse_rotation_line(line))
    return rotations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='01')
    parser.add_argument('file', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    rotations = get_inputs(args.file)

    safe = SafeState(dial_size=100, current_position=50)
    positions = safe.apply_rotations(rotations)

    print("Part 1: number of zeros in positions")
    num_zeros = positions.count(0)
    print(num_zeros)

    print("Part 2: total zero crossings during rotations")
    total_zero_crossings = safe.get_zero_crossings()
    print(total_zero_crossings + num_zeros)