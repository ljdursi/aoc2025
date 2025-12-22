#!/usr/bin/env python3
"""
Unit tests for Advent of Code 2025 - Day 10: Click the Factory Buttons
"""
import unittest
from day10 import ButtonProblem


class TestButtonProblemParsing(unittest.TestCase):
    """Test parsing of button problem input"""

    def test_parse_example1(self):
        """Test parsing first example: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"""
        problem = ButtonProblem.from_string("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")

        # Should have 4 indicator lights
        self.assertEqual(problem.n_indicators, 4)

        # Should have 6 buttons
        self.assertEqual(problem.n_buttons, 6)

        # Goal state should be [.##.] = [False, True, True, False]
        self.assertEqual(problem.goal, [False, True, True, False])

        # Joltages should be parsed (though not used for part 1)
        self.assertEqual(problem.joltages, [3, 5, 4, 7])

    def test_parse_example2(self):
        """Test parsing second example: [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"""
        problem = ButtonProblem.from_string("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}")

        # Should have 5 indicator lights
        self.assertEqual(problem.n_indicators, 5)

        # Should have 5 buttons
        self.assertEqual(problem.n_buttons, 5)

        # Goal state should be [...#.] = [False, False, False, True, False]
        self.assertEqual(problem.goal, [False, False, False, True, False])

        # Joltages
        self.assertEqual(problem.joltages, [7, 5, 12, 7, 2])

    def test_parse_example3(self):
        """Test parsing third example: [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
        problem = ButtonProblem.from_string("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}")

        # Should have 6 indicator lights
        self.assertEqual(problem.n_indicators, 6)

        # Should have 4 buttons
        self.assertEqual(problem.n_buttons, 4)

        # Goal state should be [.###.#] = [False, True, True, True, False, True]
        self.assertEqual(problem.goal, [False, True, True, True, False, True])

        # Joltages
        self.assertEqual(problem.joltages, [10, 11, 11, 5, 10, 5])


class TestPart1BFS(unittest.TestCase):
    """Test Part 1: Binary button presses using BFS"""

    def test_example1(self):
        """
        Example 1: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        Expected: 2 presses
        """
        problem = ButtonProblem.from_string("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")
        self.assertEqual(problem.find_minimum_presses_part1(), 2)

    def test_example2(self):
        """
        Example 2: [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        Expected: 3 presses
        """
        problem = ButtonProblem.from_string("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}")
        self.assertEqual(problem.find_minimum_presses_part1(), 3)

    def test_example3(self):
        """
        Example 3: [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        Expected: 2 presses
        """
        problem = ButtonProblem.from_string("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}")
        self.assertEqual(problem.find_minimum_presses_part1(), 2)


class TestPart2ILP(unittest.TestCase):
    """Test Part 2: Integer button presses using ILP"""

    def test_example1(self):
        """
        Example 1: {3,5,4,7}
        Expected: 10 presses
        """
        problem = ButtonProblem.from_string("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")
        self.assertEqual(problem.find_minimum_presses_part2(), 10)

    def test_example2(self):
        """
        Example 2: {7,5,12,7,2}
        Expected: 12 presses
        """
        problem = ButtonProblem.from_string("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}")
        self.assertEqual(problem.find_minimum_presses_part2(), 12)

    def test_example3(self):
        """
        Example 3: {10,11,11,5,10,5}
        Expected: 11 presses
        """
        problem = ButtonProblem.from_string("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}")
        self.assertEqual(problem.find_minimum_presses_part2(), 11)

    def test_large_values(self):
        """
        Test with large target values that would be intractable for BFS.
        Targets: {25,23,28,53,34,54,41,12,28,22}
        Expected: 74 presses
        """
        problem = ButtonProblem.from_string(
            "[#...#.#.#.] (2,3,5,6,7,8) (3,4,5) (1,3,4,5,6,9) (2,3,6,8) "
            "(3,5,6,7,8) (0,5) (0,2,3,4,6,7,8,9) (0,1,2,8) {25,23,28,53,34,54,41,12,28,22}"
        )
        self.assertEqual(problem.find_minimum_presses_part2(), 74)


if __name__ == '__main__':
    unittest.main()
