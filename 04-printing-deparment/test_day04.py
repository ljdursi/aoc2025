#!/usr/bin/env python3
"""
Tests for Advent of Code 2025 - Day 4: Printing Department
"""
import unittest
from day04 import Map


class TestPrintingDepartment(unittest.TestCase):
    """Test suite for the printing department map and roll removal functionality."""

    # Example map from the problem statement
    EXAMPLE_MAP = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]

    def test_example_accessible_rolls(self):
        """
        Test the example from the problem statement.

        According to the problem: "there are 13 rolls of paper that can be accessed
        by a forklift" - these are rolls with fewer than 4 neighboring rolls.

        The marked example shows:
        ..xx.xx@x.
        x@@.@.@.@@
        @@@@@.x.@@
        @.@@@@..@.
        x@.@@@@.@x
        .@@@@@@@.@
        .@.@.@.@@@
        x.@@@.@@@@
        .@@@@@@@@.
        x.x.@@@.x.

        Where 'x' marks accessible rolls (@ with < 4 @ neighbors).
        """
        # Expected accessible coordinates (row, col) - 0-indexed
        # Extracted from the marked example by comparing @ -> x positions
        expected_accessible = [
            (0, 2), (0, 3), (0, 5), (0, 6), (0, 8),  # Row 0: ..xx.xx@x.
            (1, 0),                                    # Row 1: x@@.@.@.@@
            (2, 6),                                    # Row 2: @@@@@.x.@@
                                                       # Row 3: @.@@@@..@. (none)
            (4, 0), (4, 9),                           # Row 4: x@.@@@@.@x
                                                       # Row 5: .@@@@@@@.@ (none)
                                                       # Row 6: .@.@.@.@@@ (none)
            (7, 0),                                    # Row 7: x.@@@.@@@@
                                                       # Row 8: .@@@@@@@@. (none)
            (9, 0), (9, 2), (9, 8),                   # Row 9: x.x.@@@.x.
        ]

        map_obj = Map(self.EXAMPLE_MAP)
        accessible = map_obj.accessible_cells()

        # Check the exact coordinates (order doesn't matter, so convert to sets)
        self.assertEqual(set(accessible), set(expected_accessible),
                        f"Accessible coordinates don't match.\n"
                        f"Expected: {sorted(expected_accessible)}\n"
                        f"Got: {sorted(accessible)}")

    def test_example_specific_cells(self):
        """
        Test specific cells to verify the neighbor counting logic.
        """
        map_obj = Map(self.EXAMPLE_MAP)

        # Test a few specific cells
        # (0, 2) should be accessible: @ with 3 neighbors: (0,3), (1,1), (1,2)
        self.assertEqual(map_obj.n_neighbours(0, 2), 3,
                        "Cell (0,2) should have 3 neighbors")

        # (0, 7) should NOT be accessible: @ with 4 neighbors
        self.assertEqual(map_obj.n_neighbours(0, 7), 4,
                        "Cell (0,7) should have 4 neighbors")

        # (1, 0) should be accessible: @ with 3 neighbors
        self.assertEqual(map_obj.n_neighbours(1, 0), 3,
                        "Cell (1,0) should have 3 neighbors")

    def test_edge_cases(self):
        """
        Test edge cases like corners and single rolls.
        """
        # Single roll - should be accessible (0 neighbors)
        single_roll = ["@"]
        map_obj = Map(single_roll)
        self.assertEqual(len(map_obj.accessible_cells()), 1)

        # Roll in corner with 3 neighbors - should be accessible
        corner_test = [
            "@@",
            "@@",
        ]
        map_obj = Map(corner_test)
        # All 4 rolls have 3 neighbors each, so all should be accessible
        self.assertEqual(len(map_obj.accessible_cells()), 4)

        # 3x3 grid with center having 8 neighbors - center should NOT be accessible
        dense_grid = [
            "@@@",
            "@@@",
            "@@@",
        ]
        map_obj = Map(dense_grid)
        accessible = map_obj.accessible_cells()
        # Center cell (1,1) has 8 neighbors, should not be accessible
        self.assertNotIn((1, 1), accessible)
        # Corner cells have 3 neighbors each, should be accessible
        self.assertIn((0, 0), accessible)
        self.assertIn((0, 2), accessible)
        self.assertIn((2, 0), accessible)
        self.assertIn((2, 2), accessible)

    def test_remove_roll_basic(self):
        """
        Test basic remove_roll functionality.
        """
        input_map = [
            "@@@",
            "@@@",
            "@@@",
        ]
        map_obj = Map(input_map)

        # Remove a corner roll
        result = map_obj.remove_roll(0, 0)
        self.assertTrue(result, "Should successfully remove a roll")
        self.assertEqual(map_obj.grid[0][0], '.', "Cell should be empty after removal")

        # Try to remove the same cell again
        result = map_obj.remove_roll(0, 0)
        self.assertFalse(result, "Should fail to remove an empty cell")

    def test_remove_roll_updates_neighbors(self):
        """
        Test that removing a roll updates neighbor counts correctly.
        """
        input_map = [
            "@@@",
            "@@@",
            "@@@",
        ]
        map_obj = Map(input_map)

        # Before removal: center cell (1,1) has 8 neighbors
        self.assertEqual(map_obj.neighbour_count[1][1], 8)
        self.assertFalse(map_obj.accessible[1][1], "Center should not be accessible")

        # Remove corner cell (0,0)
        map_obj.remove_roll(0, 0)

        # After removal: center cell should have 7 neighbors
        self.assertEqual(map_obj.neighbour_count[1][1], 7)
        # Cell at (0,1) should have gone from 5 to 4 neighbors
        self.assertEqual(map_obj.neighbour_count[0][1], 4)
        # Cell at (1,0) should have gone from 5 to 4 neighbors
        self.assertEqual(map_obj.neighbour_count[1][0], 4)

    def test_remove_roll_makes_new_accessible(self):
        """
        Test that removing a roll can make previously inaccessible rolls accessible.
        """
        input_map = [
            "@@@",
            "@@@",
            "@@@",
        ]
        map_obj = Map(input_map)

        # Initially, only corner and edge cells are accessible (center is not)
        initial_accessible = map_obj.accessible_cells()
        self.assertNotIn((1, 1), initial_accessible)

        # Remove corner cells to reduce center's neighbor count
        map_obj.remove_roll(0, 0)
        map_obj.remove_roll(0, 2)
        map_obj.remove_roll(2, 0)
        map_obj.remove_roll(2, 2)

        # Now center should have 4 neighbors and become accessible
        accessible_after = map_obj.accessible_cells()
        # Center still has 4 neighbors (edges), so still not accessible
        # But edge cells now have fewer neighbors

        # Remove one more edge cell
        map_obj.remove_roll(0, 1)
        # Now center has 3 neighbors
        self.assertEqual(map_obj.neighbour_count[1][1], 3)
        self.assertTrue(map_obj.accessible[1][1], "Center should now be accessible")

    def test_example_iterative_removal(self):
        """
        Test the full iterative removal process from the problem statement.

        According to the problem, removing accessible rolls repeatedly should
        remove rolls in batches: 13, 12, 7, 5, 2, 1, 1, 1, 1 for a total of 43.
        """
        map_obj = Map(self.EXAMPLE_MAP)

        # Track the number removed in each iteration
        removed_per_iteration = []
        total_removed = 0

        while True:
            accessible = map_obj.accessible_cells()
            if not accessible:
                break

            # Remove all currently accessible rolls
            for (r, c) in accessible:
                map_obj.remove_roll(r, c)

            removed_per_iteration.append(len(accessible))
            total_removed += len(accessible)

        # According to the problem statement
        expected_sequence = [13, 12, 7, 5, 2, 1, 1, 1, 1]
        expected_total = sum(expected_sequence)  # 43

        self.assertEqual(removed_per_iteration, expected_sequence,
                        f"Removal sequence doesn't match.\n"
                        f"Expected: {expected_sequence}\n"
                        f"Got: {removed_per_iteration}")
        self.assertEqual(total_removed, expected_total,
                        f"Expected to remove {expected_total} rolls total, got {total_removed}")

    def test_small_iterative_removal(self):
        """
        Test iterative removal on a smaller, simpler example.
        """
        # 2x2 grid: all 4 cells have 3 neighbors, all accessible
        input_map = [
            "@@",
            "@@",
        ]

        map_obj = Map(input_map)

        # First iteration: all 4 should be accessible
        accessible = map_obj.accessible_cells()
        self.assertEqual(len(accessible), 4)

        # Remove all
        for (r, c) in accessible:
            map_obj.remove_roll(r, c)

        # No more accessible rolls
        accessible = map_obj.accessible_cells()
        self.assertEqual(len(accessible), 0)


if __name__ == "__main__":
    unittest.main()
