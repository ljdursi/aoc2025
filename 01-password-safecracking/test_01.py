#!/usr/bin/env python3
import unittest
import sys
from io import StringIO

sys.path.insert(0, '.')

from importlib import import_module
solution = import_module('01')

RotDir = solution.RotDir
Rotation = solution.Rotation
SafeState = solution.SafeState
parse_rotation_line = solution.parse_rotation_line
get_inputs = solution.get_inputs


class TestParsing(unittest.TestCase):
    """Test the parsing of rotation strings."""

    def test_parse_left_rotation(self):
        """Test parsing a left rotation."""
        rotation = parse_rotation_line("L68")
        self.assertEqual(rotation.direction, RotDir.LEFT)
        self.assertEqual(rotation.steps, 68)

    def test_parse_right_rotation(self):
        """Test parsing a right rotation."""
        rotation = parse_rotation_line("R48")
        self.assertEqual(rotation.direction, RotDir.RIGHT)
        self.assertEqual(rotation.steps, 48)

    def test_parse_with_whitespace(self):
        """Test parsing handles leading/trailing whitespace."""
        rotation = parse_rotation_line("  L30  ")
        self.assertEqual(rotation.direction, RotDir.LEFT)
        self.assertEqual(rotation.steps, 30)

    def test_parse_invalid_direction(self):
        """Test parsing raises error for invalid direction."""
        with self.assertRaises(ValueError):
            parse_rotation_line("X50")

    def test_parse_empty_line(self):
        """Test parsing raises error for empty line."""
        with self.assertRaises(ValueError):
            parse_rotation_line("")

    def test_parse_problem_example_rotations(self):
        """Test parsing all rotations from the problem example."""
        test_cases = [
            ("L68", RotDir.LEFT, 68),
            ("L30", RotDir.LEFT, 30),
            ("R48", RotDir.RIGHT, 48),
            ("L5", RotDir.LEFT, 5),
            ("R60", RotDir.RIGHT, 60),
            ("L55", RotDir.LEFT, 55),
            ("L1", RotDir.LEFT, 1),
            ("L99", RotDir.LEFT, 99),
            ("R14", RotDir.RIGHT, 14),
            ("L82", RotDir.LEFT, 82),
        ]

        for line, expected_dir, expected_steps in test_cases:
            with self.subTest(line=line):
                rotation = parse_rotation_line(line)
                self.assertEqual(rotation.direction, expected_dir)
                self.assertEqual(rotation.steps, expected_steps)

    def test_get_inputs_from_file(self):
        """Test reading multiple rotations from a file-like object."""
        input_text = """L68
L30
R48

L5
R60"""
        fileobj = StringIO(input_text)
        rotations = get_inputs(fileobj)

        self.assertEqual(len(rotations), 5)
        self.assertEqual(rotations[0].direction, RotDir.LEFT)
        self.assertEqual(rotations[0].steps, 68)
        self.assertEqual(rotations[2].direction, RotDir.RIGHT)
        self.assertEqual(rotations[2].steps, 48)


class TestRotation(unittest.TestCase):
    """Test the rotation functionality using the example from the problem definition."""

    def test_rotation_sequence(self):
        """Test the complete rotation sequence from the problem definition."""
        # Define the rotations from the problem using the parse function
        rotation_lines = [
            "L68",
            "L30",
            "R48",
            "L5",
            "R60",
            "L55",
            "L1",
            "L99",
            "R14",
            "L82",
        ]

        # Expected positions after each rotation
        expected_positions = [82, 52, 0, 95, 55, 0, 99, 0, 14, 32]

        # Start at position 50
        safe = SafeState(dial_size=100, current_position=50)

        # Verify starting position
        self.assertEqual(safe.get_position(), 50, "Dial should start at position 50")

        # Apply each rotation and check the resulting position
        for i, line in enumerate(rotation_lines):
            rotation = parse_rotation_line(line)
            safe.rotate(rotation)
            actual_position = safe.get_position()
            expected_position = expected_positions[i]

            self.assertEqual(
                actual_position,
                expected_position,
                f"After rotation {line}, expected position {expected_position} but got {actual_position}"
            )

    def test_individual_rotations(self):
        """Test each rotation individually to isolate any failures."""
        test_cases = [
            (50, "L68", 82, "L68 from 50 should reach 82"),
            (82, "L30", 52, "L30 from 82 should reach 52"),
            (52, "R48", 0, "R48 from 52 should reach 0"),
            (0, "L5", 95, "L5 from 0 should reach 95"),
            (95, "R60", 55, "R60 from 95 should reach 55"),
            (55, "L55", 0, "L55 from 55 should reach 0"),
            (0, "L1", 99, "L1 from 0 should reach 99"),
            (99, "L99", 0, "L99 from 99 should reach 0"),
            (0, "R14", 14, "R14 from 0 should reach 14"),
            (14, "L82", 32, "L82 from 14 should reach 32"),
        ]

        for start_pos, line, expected_pos, msg in test_cases:
            with self.subTest(msg=msg):
                safe = SafeState(dial_size=100, current_position=start_pos)
                rotation = parse_rotation_line(line)
                safe.rotate(rotation)
                actual_pos = safe.get_position()

                self.assertEqual(actual_pos, expected_pos, msg)


if __name__ == '__main__':
    unittest.main()
