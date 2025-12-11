#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 5: Cafeteria inventory freshness
"""

import argparse
from typing import TextIO

class Range:
    """Represents an inclusive range of integers [start, end].
       From Day 2: Gift Shop IDs."""

    def __init__(self, start: int, end: int):
        """
        Initialize a Range.

        Args:
            start: The lower bound of the range (inclusive).
            end: The upper bound of the range (inclusive).

        Raises:
            ValueError: If start > end.
        """
        if start > end:
            raise ValueError(f"Invalid range: start ({start}) > end ({end})")
        self.start = start
        self.end = end

    @classmethod
    def from_tuple(cls, t: tuple[int, int]) -> "Range":
        """Alternate constructor from (start, end)."""
        return cls(t[0], t[1])

    @classmethod
    def from_str(cls, s: str, sep: str = '-') -> "Range":
        """Alternate constructor from a string like '11-22'."""
        start_str, end_str = s.split(sep)
        return cls(int(start_str), int(end_str))

    @classmethod
    def valid_str(cls, s: str, sep: str = '-') -> bool:
        parts = s.split(sep)
        if len(parts) != 2:
            return False
        try:
            start_str, end_str = parts
            return int(start_str) <= int(end_str)
        except ValueError:
            return False

    def __str__(self):
        """Return string representation in the format 'start-end'."""
        return f"{self.start}-{self.end}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return f"Range({self.start}, {self.end})"

    def contains(self, value: int) -> bool:
        """
        Check if a value is within this range.

        Args:
            value: The integer to check.

        Returns:
            True if start <= value <= end, False otherwise.
        """
        return self.start <= value <= self.end

    def __lt__(self, other: "Range") -> bool:
        """Less-than comparison based on start value."""
        return self.start < other.start

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on start and end values."""
        if not isinstance(other, Range):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        """Return hash for use in sets and dictionaries."""
        return hash((self.start, self.end))

    def overlaps(self, other: "Range") -> bool:
        """
        Check if this range overlaps with another range.

        Args:
            other: Another Range object.
        Returns:
            True if the ranges overlap, False otherwise.
        """
        return not (self.end < other.start or self.start > other.end)

    def merge(self, other: "Range") -> "Range":
        """
        Merge this range with another overlapping range.

        Args:
            other: Another Range object that overlaps with this one.
        Returns:
            A new Range object that spans both ranges.
        Raises:
            ValueError: If the ranges do not overlap.
        """
        if not self.overlaps(other):
            raise ValueError("Ranges do not overlap and cannot be merged.")
        return Range(min(self.start, other.start), max(self.end, other.end))

    def length(self) -> int:
        """Return the length of the range."""
        return self.end - self.start + 1

def contained_in_ranges(value: int, ranges: list[Range]) -> bool:
    """
    Check if a value is contained in any of the given ranges.

    Args:
        value: The integer to check.
        ranges: A list of Range objects.
    Returns:
        True if the value is contained in any range, False otherwise.
    """
    return any(r.contains(value) for r in ranges)

def merge_ranges(ranges: list[Range]) -> list[Range]:
    """
    Merge overlapping ranges in a list.

    Args:
        ranges: A list of Range objects.
    Returns:
        A new list of Range objects with overlapping ranges merged.
    """
    if not ranges:
        return []

    # Sort ranges by start value
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last_merged = merged[-1]
        if last_merged.overlaps(current):
            # Merge overlapping ranges
            merged[-1] = last_merged.merge(current)
        else:
            merged.append(current)

    return merged

def get_inputs(fileobj: TextIO) -> tuple[list[Range], list[int]]:
    """
    Parse input file containing ranges and values.

    Each line contains either a range in the format "start-end" or a single integer value.
    Empty lines are ignored.

    Args:
        fileobj: Text file object to read from.

    Returns:
        A tuple of (ranges, values) where ranges is a list of Range objects
        and values is a list of integers.
    """
    ranges = []
    values = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        if Range.valid_str(line):
            ranges.append(Range.from_str(line))
        else:
            values.append(int(line))

    return ranges, values


def main():
    parser = argparse.ArgumentParser(prog='05', description="Cafeteria inventory freshness checker.")
    parser.add_argument('input_file', type=argparse.FileType('r'), help='Input file path')
    args = parser.parse_args()

    ranges, values = get_inputs(args.input_file)
    ranges = merge_ranges(ranges)

    fresh_count = sum(1 for v in values if contained_in_ranges(v, ranges))

    print("Part 1")
    print(fresh_count)

    print("Part 2")
    total_length = sum(r.length() for r in ranges)
    print(total_length)

         
if __name__ == '__main__':
    main()