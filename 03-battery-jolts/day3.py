#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 3: Lobby (batteries and joltage)

"""
import argparse
import sys
from typing import TextIO

def max_joltage(batteries: list[int], ndigits: int) -> int:
    """
    Calculate the maximum joltage from a bank of batteries

    Args:
        batteries: A list of integer digits representing battery values
        ndigits: The number of digits to select for the joltage

    Returns:
        The maximum joltage integer formed by selecting ndigits batteries
    """
    n = len(batteries)

    if ndigits <= 0:
        raise ValueError("ndigits must be positive")
    if ndigits > n:
        raise ValueError("ndigits must be less than or equal to the number of batteries")

    max_j = 0

    order = sorted(range(n), key=lambda i: batteries[i], reverse=True)
    leftmost = -1

    for i in range(ndigits):
        # find the highest digit further ahead than the leftmost and before or at the rightmost
        rightmost = n - (ndigits - i)
        for idx in order:
            if leftmost < idx and idx <= rightmost:
                break
        leftmost = idx
        max_j = max_j * 10 + batteries[idx]

    return max_j

def parse_batteries(line: str) -> list[int]:
    """
    Parse a line of battery digits into a list of integers.

    Args:
        line: A string of digits, e.g. "389125467"

    Returns:
        A list of integers representing the battery digits.
    """
    line = line.strip()
    return [int(char) for char in line if char.isdigit()]


def get_inputs(fileobj: TextIO) -> list[list[int]]:
    """
    Read and parse battery digits from a file-like object.

    Reads lines from the file, where each line contains a string of digits.
    Empty lines are skipped.

    Args:
        fileobj: A file-like object (or any iterator of strings) containing
                battery digit strings, one per line.
    Returns:
        A list of list of integers representing the battery digits.
    """
    batteries = []
    for line in fileobj:
        line = line.strip()
        if not line:
            continue

        batteries.append(parse_batteries(line))

    return batteries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='03', description="Calculate maximum joltage from battery banks.")
    parser.add_argument("input_file", type=argparse.FileType('r'), help="Input file containing battery digit strings.")
    args = parser.parse_args()

    batteries_list = get_inputs(args.input_file)

    print("Part 1")
    max_js = [max_joltage(batteries, 2) for batteries in batteries_list]
    print(sum(max_js))

    print("Part 2")
    max_js = [max_joltage(batteries, 12) for batteries in batteries_list]
    print(sum(max_js))