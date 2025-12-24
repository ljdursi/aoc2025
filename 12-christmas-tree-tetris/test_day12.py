#!/usr/bin/env python3
import unittest
from io import StringIO
from day12 import Shape, Requirements, Orientation, get_inputs, can_pack_trivial, Solver


class TestShape(unittest.TestCase):
    def test_shape_from_lines_simple(self):
        """Test parsing a simple shape."""
        lines = ["###", "##.", "##."]
        shape = Shape.from_lines(lines)

        # Should have 7 cells filled (3 + 2 + 2)
        self.assertEqual(len(shape.grid), 7)

        # Should be 3 wide and 3 tall
        self.assertEqual(shape.shape, (3, 3))

        # Check specific points
        self.assertIn((0, 0), shape.grid)
        self.assertIn((1, 0), shape.grid)
        self.assertIn((2, 0), shape.grid)
        self.assertIn((0, 1), shape.grid)
        self.assertIn((1, 1), shape.grid)
        self.assertNotIn((2, 1), shape.grid)

    def test_shape_from_lines_with_offset(self):
        """Test parsing a shape with dots at the start."""
        lines = [".##", "###", "##."]
        shape = Shape.from_lines(lines)

        # Should have 7 cells filled
        self.assertEqual(len(shape.grid), 7)

        # Should be 3 wide and 3 tall
        self.assertEqual(shape.shape, (3, 3))

    def test_shape_str_representation(self):
        """Test string representation of a shape."""
        lines = ["###", "#..", "###"]
        shape = Shape.from_lines(lines)
        result = str(shape)

        expected_lines = ["###", "#..", "###"]
        self.assertEqual(result, "\n".join(expected_lines))

    def test_shape_rotation_0(self):
        """Test 0 degree rotation (no rotation)."""
        lines = ["###", "#..", "##."]
        shape = Shape.from_lines(lines)
        rotated = shape.rotate(Orientation.deg_0)

        # Should be identical
        self.assertEqual(str(rotated), str(shape))

    def test_shape_rotation_90(self):
        """Test 90 degree rotation."""
        lines = ["###", "#..", "###"]
        shape = Shape.from_lines(lines)
        rotated = shape.rotate(Orientation.deg_90)

        # 90 degree rotation of:
        # ###
        # #..
        # ###
        expected = "###\n#.#\n#.#"
        self.assertEqual(str(rotated), expected)

    def test_shape_rotation_180(self):
        """Test 180 degree rotation."""
        lines = ["###", "#..", "###"]
        shape = Shape.from_lines(lines)
        rotated = shape.rotate(Orientation.deg_180)

        # 180 degree rotation should flip both axes
        expected = "###\n..#\n###"
        self.assertEqual(str(rotated), expected)

    def test_shape_rotation_270(self):
        """Test 270 degree rotation."""
        lines = ["###", "#..", "###"]
        shape = Shape.from_lines(lines)
        rotated = shape.rotate(Orientation.deg_270)

        # 270 degree rotation
        expected = "#.#\n#.#\n###"
        self.assertEqual(str(rotated), expected)

    def test_shape_all_rotations_preserve_cell_count(self):
        """Test that rotation preserves the number of cells."""
        lines = ["###", "##.", ".##"]
        shape = Shape.from_lines(lines)
        original_count = len(shape.grid)

        for orientation in Orientation:
            rotated = shape.rotate(orientation)
            self.assertEqual(len(rotated.grid), original_count,
                           f"Rotation {orientation} changed cell count")


class TestRequirements(unittest.TestCase):
    def test_requirements_from_str_simple(self):
        """Test parsing a simple requirements line."""
        line = "4x4: 0 0 0 0 2 0"
        req = Requirements.from_str(line)

        self.assertEqual(req.size, (4, 4))
        self.assertEqual(req.counts, [0, 0, 0, 0, 2, 0])

    def test_requirements_from_str_complex(self):
        """Test parsing a more complex requirements line."""
        line = "12x5: 1 0 1 0 2 2"
        req = Requirements.from_str(line)

        self.assertEqual(req.size, (12, 5))
        self.assertEqual(req.counts, [1, 0, 1, 0, 2, 2])

    def test_requirements_str_representation(self):
        """Test string representation of requirements."""
        line = "12x5: 1 0 1 0 2 2"
        req = Requirements.from_str(line)

        self.assertEqual(str(req), line)

    def test_requirements_invalid_size(self):
        """Test that invalid size format raises error."""
        line = "4x4x4: 1 2 3"
        with self.assertRaises(ValueError):
            Requirements.from_str(line)


class TestGetInputs(unittest.TestCase):
    def test_get_inputs_example(self):
        """Test parsing the full example input."""
        input_text = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
        fileobj = StringIO(input_text)
        shapes, requirements = get_inputs(fileobj)

        # Should have 6 shapes
        self.assertEqual(len(shapes), 6)

        # Should have 3 requirements
        self.assertEqual(len(requirements), 3)

        # Check first shape (shape 0)
        self.assertEqual(shapes[0].shape, (3, 3))
        self.assertEqual(len(shapes[0].grid), 7)

        # Check last shape (shape 5: ###, .#., ###)
        self.assertEqual(shapes[5].shape, (3, 3))
        self.assertEqual(len(shapes[5].grid), 7)  # 3 + 1 + 3 = 7 cells

        # Check first requirement
        self.assertEqual(requirements[0].size, (4, 4))
        self.assertEqual(requirements[0].counts, [0, 0, 0, 0, 2, 0])

        # Check last requirement
        self.assertEqual(requirements[2].size, (12, 5))
        self.assertEqual(requirements[2].counts, [1, 0, 1, 0, 3, 2])

    def test_get_inputs_single_shape(self):
        """Test parsing input with a single shape."""
        input_text = """0:
###
#..

4x4: 1
"""
        fileobj = StringIO(input_text)
        shapes, requirements = get_inputs(fileobj)

        self.assertEqual(len(shapes), 1)
        self.assertEqual(len(requirements), 1)
        self.assertEqual(shapes[0].shape, (3, 2))
        self.assertEqual(requirements[0].counts, [1])

    def test_get_inputs_no_blank_lines_between_shapes(self):
        """Test parsing when shapes aren't separated by blank lines."""
        input_text = """0:
###
1:
#.#
###

2x2: 1 1
"""
        fileobj = StringIO(input_text)
        shapes, requirements = get_inputs(fileobj)

        self.assertEqual(len(shapes), 2)
        self.assertEqual(shapes[0].shape, (3, 1))
        self.assertEqual(shapes[1].shape, (3, 2))


class TestTrivialPacking(unittest.TestCase):
    def setUp(self):
        """Create a set of 3x3 shapes with 7 cells each."""
        self.shapes = [
            Shape.from_lines(["###", "##.", "##."]),  # Shape 0
            Shape.from_lines(["###", "#..", "###"]),  # Shape 1
        ]

    def test_trivial_no_too_many_cells(self):
        """Test trivial NO: need more cells than available."""
        # 10x10 grid = 100 cells, but need 20 shapes * 7 cells = 140 cells
        req = Requirements((10, 10), [10, 10])
        result = can_pack_trivial(self.shapes, req)
        self.assertFalse(result)

    def test_trivial_no_exact_boundary(self):
        """Test trivial NO: need exactly one more cell than available."""
        # 7x7 grid = 49 cells, but need 8 shapes * 7 cells = 56 cells
        req = Requirements((7, 7), [4, 4])
        result = can_pack_trivial(self.shapes, req)
        self.assertFalse(result)

    def test_trivial_yes_plenty_of_regions(self):
        """Test trivial YES: plenty of 3x3 regions for all shapes."""
        # 12x12 grid has 4x4 = 16 non-overlapping 3x3 regions
        # Only need 10 shapes total
        req = Requirements((12, 12), [5, 5])
        result = can_pack_trivial(self.shapes, req)
        self.assertTrue(result)

    def test_trivial_yes_exact_regions(self):
        """Test trivial YES: exactly enough 3x3 regions."""
        # 9x9 grid has 3x3 = 9 non-overlapping 3x3 regions
        # Need exactly 9 shapes
        req = Requirements((9, 9), [5, 4])
        result = can_pack_trivial(self.shapes, req)
        self.assertTrue(result)

    def test_needs_solving_more_shapes_than_regions(self):
        """Test that returns None when more shapes than regions but enough cells."""
        # 6x6 grid has 2x2 = 4 non-overlapping 3x3 regions
        # Need 5 shapes * 7 cells = 35 cells, grid has 36 cells
        # So enough cells, but more shapes than grid regions
        req = Requirements((6, 6), [3, 2])
        result = can_pack_trivial(self.shapes, req)
        self.assertIsNone(result)

    def test_trivial_yes_no_shapes(self):
        """Test trivial YES: no shapes to place."""
        req = Requirements((5, 5), [0, 0])
        result = can_pack_trivial(self.shapes, req)
        self.assertTrue(result)


class TestSolver(unittest.TestCase):
    def setUp(self):
        """Create shapes for testing."""
        self.shapes = [
            Shape.from_lines(["###", "##.", "##."]),  # Shape 0
            Shape.from_lines(["###", "#..", "###"]),  # Shape 1
        ]

    def test_solver_simple_solvable(self):
        """Test solver on simple solvable case: 2 shapes in 4x4 grid."""
        # Only using shape at index 1, 2 copies
        req = Requirements((4, 4), [0, 2])
        solver = Solver(self.shapes, req)
        result = solver.solve()
        self.assertTrue(result)

    def test_solver_no_shapes(self):
        """Test solver with no shapes to place."""
        req = Requirements((5, 5), [0, 0])
        solver = Solver(self.shapes, req)
        result = solver.solve()
        self.assertTrue(result)

    def test_solver_single_shape_fits(self):
        """Test solver with single shape that fits."""
        req = Requirements((3, 3), [1, 0])
        solver = Solver(self.shapes, req)
        result = solver.solve()
        self.assertTrue(result)

    def test_solver_too_many_cells_needed(self):
        """Test solver fails when too many cells needed."""
        # Grid is 3x3 = 9 cells, but need 2 shapes * 7 cells = 14 cells
        req = Requirements((3, 3), [1, 1])
        solver = Solver(self.shapes, req)
        result = solver.solve()
        self.assertFalse(result)

    def test_solver_exact_fill(self):
        """Test solver with shapes that exactly fill the grid."""
        # Create a simple 2-cell shape
        small_shapes = [Shape.from_lines(["##"])]
        # 2x2 grid = 4 cells, use 2 shapes of 2 cells each
        req = Requirements((2, 2), [2])
        solver = Solver(small_shapes, req)
        result = solver.solve()
        self.assertTrue(result)

    def test_solver_from_ex01_first_case(self):
        """Test the actual first case from ex01.txt."""
        # Load the actual shapes from ex01.txt format
        shapes = [
            Shape.from_lines(["###", ".#.", "###"]),  # Shape 0
            Shape.from_lines(["###", "#..", "###"]),  # Shape 1
            Shape.from_lines(["###", "##.", ".##"]),  # Shape 2
            Shape.from_lines(["..#", "###", "###"]),  # Shape 3
            Shape.from_lines([".##", "##.", "#.."]),  # Shape 4
            Shape.from_lines(["###", "##.", "#.."]),  # Shape 5
        ]
        # First requirement: 4x4 with 2 copies of shape 4
        req = Requirements((4, 4), [0, 0, 0, 0, 2, 0])
        solver = Solver(shapes, req)
        result = solver.solve()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
