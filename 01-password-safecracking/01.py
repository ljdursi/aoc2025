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

    def rotate(self, rotation: Rotation):
        direction, steps = rotation.direction, rotation.steps
        rot_start = self.current_position

        n_zeros = steps // self.dial_size
        steps = steps % self.dial_size

        if direction == RotDir.LEFT:
            rot_end = (rot_start - steps) % self.dial_size
            if steps > rot_start and rot_start != 0 and rot_end != 0:
                n_zeros += 1
        elif direction == RotDir.RIGHT:
            rot_end = (rot_start + steps) % self.dial_size
            if steps > (self.dial_size - rot_start) and rot_start != 0 and rot_end != 0:
                n_zeros += 1

        self.current_position = rot_end
        self.zero_crossings += n_zeros

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

def get_inputs(fileobj: TextIO) -> list[Rotation]:
    # reads lines of the form "L3" or "R5" from fileobj
    rotations = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        direction_char = line[0]
        steps = int(line[1:])

        if direction_char == 'L':
            direction = RotDir.LEFT
        elif direction_char == 'R':
            direction = RotDir.RIGHT
        else:
            raise ValueError(f"Invalid direction character: {direction_char}")

        rotations.append(Rotation(direction, steps))
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