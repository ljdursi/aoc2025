#!/usr/bin/env python3
import argparse
import sys
from enum import Enum
from typing import TextIO

class RotDir(Enum):
    LEFT = -1
    RIGHT = 1

class Rotation(object):
    def __init__(self, direction: RotDir, steps: int):
        self.direction = direction
        self.steps = steps

    def __str__(self):
        dir_char = 'L' if self.direction == RotDir.LEFT else 'R'
        return f"{dir_char}{self.steps}"

class SafeState(object):
    def __init__(self, dial_size: int=100, current_position: int = 0):
        self.dial_size = dial_size
        self.current_position = current_position % dial_size
        self.zero_crossings = 0

    def _count_multiples_between(self, start: int, end: int, multiple: int) -> int:
        """Count how many multiples of 'multiple' exist strictly between start and end."""
        min_pos, max_pos = min(start, end), max(start, end)
        first = (min_pos // multiple + 1) * multiple
        last = max_pos // multiple * multiple
        if max_pos % multiple == 0:
            last -= multiple
        return max(0, (last - first) // multiple + 1)

    def rotate(self, rotation: Rotation):
        start = self.current_position
        end = start + (rotation.steps if rotation.direction == RotDir.RIGHT else -rotation.steps)

        self.zero_crossings += self._count_multiples_between(start, end, self.dial_size)
        self.current_position = end % self.dial_size

    def get_position(self) -> int:
        return self.current_position

    def get_zero_crossings(self) -> int:
        return self.zero_crossings

    def apply_rotations(self, rotations: list[Rotation]) -> list[int]:
        positions = []
        for rotation in rotations:
            self.rotate(rotation)
            positions.append(self.get_position())

        return positions

def parse_rotation_line(line: str) -> Rotation:
    """Parse a single line like 'L3' or 'R5' into a Rotation object."""
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
    """Reads lines of the form 'L3' or 'R5' from fileobj."""
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