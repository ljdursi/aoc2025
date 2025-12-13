#!/usr/bin/env python3
"""
Unit tests for Advent of Code 2025 - Day 7: Tachyon Splitting
"""
import unittest
from io import StringIO
from day07 import Map, get_inputs, count_paths_to_exit


class TestTachyonSplitting(unittest.TestCase):
    """Test cases for tachyon beam splitting."""

    def _run_test(self, input_text: str, expected_splitters: int = None, expected_paths: int = None):
        """
        Helper method to run a test case with given input.

        Args:
            input_text: The map layout as a string
            expected_splitters: Expected number of splitters hit (None to skip check)
            expected_paths: Expected number of distinct paths (None to skip check)

        Returns:
            Tuple of (splitters_hit, paths, total_paths)
        """
        lab_map = get_inputs(StringIO(input_text))
        splitters_hit, paths = lab_map.propagate()
        total_paths = count_paths_to_exit(lab_map, paths)

        if expected_splitters is not None:
            self.assertEqual(len(splitters_hit), expected_splitters,
                           f"Expected {expected_splitters} splitters hit, got {len(splitters_hit)}")

        if expected_paths is not None:
            self.assertEqual(total_paths, expected_paths,
                           f"Expected {expected_paths} paths to exit, got {total_paths}")

        return splitters_hit, paths, total_paths

    # ===== Basic Tests =====

    def test_no_splitters(self):
        """Test case with no splitters - beam goes straight through."""
        input_text = """..S..
.....
.....
....."""
        self._run_test(input_text, expected_splitters=0, expected_paths=1)

    def test_simple_single_splitter(self):
        """Test a simple case with one splitter."""
        input_text = """..S..
.....
..^..
....."""
        self._run_test(input_text, expected_splitters=1, expected_paths=2)

    def test_two_splitters_in_line(self):
        """Test two splitters in the same column."""
        input_text = """..S..
.....
..^..
.....
..^..
....."""
        # First splitter is hit, creates two beams going left and right
        # Those beams exit without hitting more splitters
        self._run_test(input_text, expected_splitters=1)

    # ===== Examples from Problem =====

    def test_example1_splitters_and_paths(self):
        """Test the first example from the problem - 21 splitters hit, 40 paths."""
        input_text = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
        self._run_test(input_text, expected_splitters=21, expected_paths=40)

    def test_example2_splitters_and_paths(self):
        """Test the second example - 3 splitters hit, 4 paths."""
        input_text = """....S....
.........
....^....
.........
...^.^...
........."""
        self._run_test(input_text, expected_splitters=3, expected_paths=4)

    # ===== Convergence Tests =====

    def test_convergent_paths(self):
        """Test case where multiple paths converge to same exit column."""
        input_text = """...S...
.......
...^...
.......
..^.^..
......."""
        # S -> (2,3) splits to (3,2) and (3,4)
        # (3,2) -> (4,2) splits to (5,1) and (5,3)
        # (3,4) -> (4,4) splits to (5,3) and (5,5)
        # So 4 paths: exit at cols 1, 3, 3, 5 (4 total paths, 3 unique exits)
        self._run_test(input_text, expected_splitters=3, expected_paths=4)

    def test_three_levels_path_count(self):
        """Test three levels of splitters - should give 8 paths (2^3)."""
        input_text = """....S....
.........
....^....
.........
...^.^...
.........
..^.^.^.."""
        # With 3 levels of splitters, expect 2^3 = 8 paths
        self._run_test(input_text, expected_splitters=6, expected_paths=8)

    def test_diamond_pattern(self):
        """Test diamond: paths split, converge, then split again.

        This tests that the row-based topological sort correctly handles convergence
        followed by divergence. The original BFS approach would undercount.
        """
        input_text = """...S...
.......
...^...
.......
..^.^..
.......
...^...
.......
..^.^..
......."""
        self._run_test(input_text, expected_splitters=6, expected_paths=10)

    def test_asymmetric_convergence(self):
        """Test where branches with different path counts converge.

        This stresses the row-based topological sort - one branch may have more paths
        than another before they meet.
        """
        input_text = """....S....
.........
....^....
.........
...^.^...
.........
....^....
........."""
        self._run_test(input_text, expected_splitters=4, expected_paths=6)

    def test_wide_diamond_multiple_convergence(self):
        """Test multiple paths converging at same point.

        This creates a wide diamond pattern where 4 paths converge to a center
        point, then split again. Tests handling of multiple incoming edges.
        """
        input_text = """.....S.....
...........
.....^.....
...........
....^.^....
...........
...^...^...
...........
....^.^....
...........
.....^.....
..........."""
        self._run_test(input_text, expected_splitters=8, expected_paths=12)

    # ===== Edge Cases =====

    def test_splitter_in_last_row(self):
        """Test splitter in the very last row of the map.

        Edge case: splitter creates beams that start already off the map.
        """
        input_text = """..S..
.....
..^.."""
        self._run_test(input_text, expected_splitters=1, expected_paths=2)

    def test_beam_exits_left_edge(self):
        """Test beam that exits from the left edge.

        Verifies that beams going off the left side (col < 0) are handled correctly.
        """
        input_text = """S......
.......
^......
......."""
        self._run_test(input_text, expected_splitters=1, expected_paths=2)


if __name__ == '__main__':
    unittest.main()
