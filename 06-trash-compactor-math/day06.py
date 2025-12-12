#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 6: Trash Compactor Cephalopod Math
Refactored for improved testability
"""

import argparse
from typing import TextIO
from enum import Enum
import re
import operator
from functools import reduce


class Operation(Enum):
    ADD = '+'
    MULTIPLY = '*'

    @classmethod
    def from_str(cls, s: str) -> "Operation":
        """Alternate constructor from a string like '+' or '*'."""
        for op in cls:
            if op.value == s:
                return op
        raise ValueError(f"Invalid operation string: {s}")

    @classmethod
    def valid_str(cls, s: str) -> bool:
        """Check if a string is a valid operation."""
        return any(op.value == s for op in cls)

    @classmethod
    def values_list(cls) -> list[str]:
        """Return a list of operation values."""
        return [e.value for e in cls]

    def operator(self):
        """Return the corresponding operator function."""
        ops = {
            Operation.ADD: operator.add,
            Operation.MULTIPLY: operator.mul,
        }
        return ops[self]

    def apply(self, values: list[int]) -> int:
        """Apply the operation to a list of integers."""
        return reduce(self.operator(), values)


def find_operator_positions(operation_line: str) -> list[tuple[int, str]]:
    """
    Find the positions of operators in the operation line.

    Args:
        operation_line: The line containing operation symbols

    Returns:
        List of (position, operator) tuples where position is the column index
    """
    valid_ops = Operation.values_list()
    return [(i, char) for i, char in enumerate(operation_line) if char in valid_ops]


def determine_column_boundaries(operator_positions: list[tuple[int, str]], max_width: int) -> list[tuple[int, int]]:
    """
    Determine column boundaries based on operator positions.

    Each operator marks the start of a column. Columns extend from the operator
    position to one position before the next operator (leaving a gap), or to the
    end of the line for the last column.

    Args:
        operator_positions: List of (position, operator) tuples
        max_width: Maximum width of the grid

    Returns:
        List of (start, end) tuples for each column (end is exclusive)
    """
    if not operator_positions:
        return []

    boundaries = []
    positions = [pos for pos, _ in operator_positions]

    for i, start in enumerate(positions):
        # Columns are separated by single-space gaps
        # End at position before next operator, or at line end
        if i + 1 < len(positions):
            end = positions[i + 1] - 1  # Leave gap before next column
        else:
            end = max_width
        boundaries.append((start, end))

    return boundaries


def parse_column(column_lines: list[str], cephalopod: bool) -> list[int]:
    """
    Parse a single column (vertical problem) into values.

    In normal mode, each line is read as a number.
    In cephalopod mode, the column is transposed: each character position
    (reading right-to-left) forms a number by reading top-to-bottom.

    Args:
        column_lines: List of strings, one per row, representing one column
                     (excluding the operation line)
        cephalopod: If True, transpose the column to read character positions
                   vertically

    Returns:
        List of integer values found in the column
    """
    values = []

    if cephalopod:
        # Transpose: each character position becomes a vertical number
        # Example: ['64 ', '23 ', '314'] → ['623', '431', '4']
        column_lines = [''.join(chars) for chars in zip(*column_lines)]

    for line in column_lines:
        line = line.strip()
        if not line:
            continue

        if re.match(r'^\d+$', line):
            values.append(int(line))

    return values


def parse_worksheet(text: str, cephalopod: bool=False) -> list[tuple[list[int], Operation]]:
    """
    Parse worksheet text into problems, preserving column alignment.

    The last line contains operators that mark the start of each column.
    Columns extend from each operator position to just before the next operator.

    Args:
        text: The full worksheet text
        cephalopod: If True, parse in cephalopod mode (transpose columns to read
                   character positions vertically)

    Returns:
        List of (values, operation) tuples, one per problem
    """
    # Read lines without stripping (preserve spacing!)
    lines = [line.rstrip('\n') for line in text.split('\n') if line.strip()]

    if not lines:
        return []

    # Last line contains the operations
    operation_line = lines[-1]
    value_lines = lines[:-1]

    # Find operator positions in the last line
    operator_positions = find_operator_positions(operation_line)

    if not operator_positions:
        raise ValueError("No operators found in worksheet")

    # Determine column boundaries
    max_width = max(len(line) for line in lines)
    column_boundaries = determine_column_boundaries(operator_positions, max_width)

    # Extract and parse each column
    problems = []
    for (start, end), (_, op_char) in zip(column_boundaries, operator_positions):
        # Extract this column from all value lines
        column_lines = [line[start:end] if start < len(line) else '' for line in value_lines]

        # Parse the values
        values = parse_column(column_lines, cephalopod)

        # Create the operation
        operation = Operation.from_str(op_char)

        problems.append((values, operation))

    return problems


def get_inputs(fileobj: TextIO, cephalopod: bool=False) -> list[tuple[list[int], Operation]]:
    """
    Parse input file containing a cephalopod math worksheet.

    Args:
        fileobj: Text file object to read from
        cephalopod: If True, parse in cephalopod mode (transpose columns)

    Returns:
        A list of (values, operation) tuples where values is a list of integers
        and operation is an Operation enum
    """
    text = fileobj.read()
    return parse_worksheet(text, cephalopod=cephalopod)


def calculate_grand_total(problems: list[tuple[list[int], Operation]]) -> int:
    """Calculate the sum of all problem results."""
    return sum(op.apply(vals) for vals, op in problems)


def main():
    parser = argparse.ArgumentParser(prog='06', description="Cephalopod spreadsheet calculator.")
    parser.add_argument('input_file', type=argparse.FileType('r'), help='Input file path')
    args = parser.parse_args()

    worksheet = args.input_file.read()

    print("Part 1")
    problems = parse_worksheet(worksheet, cephalopod=False)
    print(calculate_grand_total(problems))

    print("Part 2")
    problems = parse_worksheet(worksheet, cephalopod=True)
    print(calculate_grand_total(problems))


if __name__ == '__main__':
    main()
