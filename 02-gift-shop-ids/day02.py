#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 2: Gift Shop IDs

This script identifies invalid product IDs in given ranges. An invalid ID is
one that consists of a sequence of digits repeated at least twice. For example:
- 11 is invalid (1 repeated twice)
- 123123 is invalid (123 repeated twice)
- 1212121212 is invalid (12 repeated five times)

Part 1: Find invalid IDs with exactly 2 repetitions.
Part 2: Find invalid IDs with 2 or more repetitions.
"""
import argparse
import sys
from itertools import count, takewhile
from typing import TextIO, Iterator


class Range(object):
    """Represents an inclusive range of integers [start, end]."""

    def __init__(self, start: int, end: int):
        """
        Initialize a Range.

        Args:
            start: The lower bound of the range (inclusive).
            end: The upper bound of the range (inclusive).
        """
        self.start = start
        self.end = end

    def __str__(self):
        """Return string representation in the format 'start-end'."""
        return f"{self.start}-{self.end}"

    def contains(self, value: int) -> bool:
        """
        Check if a value is within this range.

        Args:
            value: The integer to check.

        Returns:
            True if start <= value <= end, False otherwise.
        """
        return self.start <= value <= self.end


def get_inputs(fileobj: TextIO) -> list[Range]:
    """
    Parse input file containing comma-separated ranges.

    Each line contains one or more ranges in the format "start-end,start-end,...".
    Empty lines are ignored.

    Args:
        fileobj: Text file object to read from.

    Returns:
        List of Range objects parsed from the input.

    Example:
        Input line: "11-22,95-115,998-1012"
        Returns: [Range(11, 22), Range(95, 115), Range(998, 1012)]
    """
    input_ranges = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        ranges = line.split(',')
        for range_str in ranges:
            input_ranges.append(Range(*map(int, range_str.split('-'))))

    return input_ranges


def digit_concatenations(r: Range, ncopies: int=2) -> Iterator[int]:
    """
    Generate invalid IDs in a range that are made of a digit sequence repeated exactly ncopies times.

    An invalid ID is a number formed by repeating a base digit sequence. For example:
    - 11 = "1" repeated 2 times
    - 123123 = "123" repeated 2 times
    - 1212121212 = "12" repeated 5 times

    The function efficiently generates these numbers without checking every number in the range.

    Args:
        r: The range to search within.
        ncopies: The number of times the base sequence should be repeated.

    Yields:
        Invalid IDs within the range, in ascending order.

    Example:
        >>> list(digit_concatenations(Range(11, 22), 2))
        [11, 22]
        >>> list(digit_concatenations(Range(95, 115), 3))
        [111]
    """
    # Determine the length of the base digit sequence
    # For a range starting at 1188511880, with ncopies=2, we want base length 5 (11885)
    length = len(str(r.start)) // ncopies
    start = int(str(r.start)[:length]) if length > 0 else 0

    # If the range start doesn't evenly divide by ncopies, round up the length
    # This ensures we start with a base number that, when repeated, is large enough
    if len(str(r.start)) % ncopies != 0:
        length += ncopies - (len(str(r.start)) % ncopies)
        start = 10**(length-1)  # Start at the smallest number with this many digits

    def make_candidate(i):
        """Create an invalid ID by repeating the digits of i exactly ncopies times."""
        return int(str(i) * ncopies)

    # Generate candidates starting from 'start', filtering to ensure they're >= r.start
    candidates = (make_candidate(i) for i in count(start) if make_candidate(i) >= r.start)
    # Yield candidates while they're still within the range
    yield from takewhile(r.contains, candidates)


def find_all_invalid_ids(r: Range) -> set[int]:
    """
    Find all invalid IDs in a range with 2 or more repetitions.

    This function searches for invalid IDs with any number of repetitions
    (2, 3, 4, ...) by checking all possible repetition counts that could
    fit within the range.

    Args:
        r: The range to search within.

    Returns:
        Set of all invalid IDs found in the range.

    Example:
        >>> sorted(find_all_invalid_ids(Range(95, 115)))
        [99, 111]
        >>> sorted(find_all_invalid_ids(Range(998, 1012)))
        [999, 1010]
    """
    invalid_ids = set()
    # Check all possible repetition counts from 2 up to the number of digits in range.end
    # (No need to check beyond that, as those numbers would be too large)
    for ncopies in range(2, len(str(r.end)) + 1):
        invalid_ids.update(digit_concatenations(r, ncopies))
    return invalid_ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='02',
        description='Find invalid product IDs (repeated digit patterns) in given ranges'
    )
    parser.add_argument('file', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file containing ranges (default: stdin)')
    args = parser.parse_args()

    ranges = get_inputs(args.file)

    # Part 1: Sum of all invalid IDs with exactly 2 repetitions
    print("Part 1")
    tot = sum(sum(digit_concatenations(r, 2)) for r in ranges)
    print(tot)

    # Part 2: Sum of all invalid IDs with 2 or more repetitions
    print("Part 2")
    tot = sum(sum(find_all_invalid_ids(r)) for r in ranges)
    print(tot)