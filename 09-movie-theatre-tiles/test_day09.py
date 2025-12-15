#!/usr/bin/env python3
"""
Unit tests for Advent of Code 2025 - Day 9: Movie Theatre Tiles
"""
import unittest
from io import StringIO
from day09 import Point, Edge, Polygon, get_inputs


class TestPoint(unittest.TestCase):
    """Test the Point class"""

    def test_point_creation(self):
        """Test basic point creation"""
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 4)

    def test_point_equality(self):
        """Test that points with same coords are equal"""
        p1 = Point(3, 4)
        p2 = Point(3, 4)
        p3 = Point(4, 3)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_point_area_simple(self):
        """Test area calculation for simple cases"""
        # Same point should give area of 1
        p = Point(0, 0)
        self.assertEqual(p.area(p), 1)

    def test_point_area_horizontal(self):
        """Test area for horizontal rectangle"""
        p1 = Point(0, 0)
        p2 = Point(3, 0)
        # Width = 4 (0,1,2,3), Height = 1 (0)
        self.assertEqual(p1.area(p2), 4)
        self.assertEqual(p2.area(p1), 4)  # Should be symmetric

    def test_point_area_vertical(self):
        """Test area for vertical rectangle"""
        p1 = Point(0, 0)
        p2 = Point(0, 3)
        # Width = 1 (0), Height = 4 (0,1,2,3)
        self.assertEqual(p1.area(p2), 4)

    def test_point_area_rectangle(self):
        """Test area for proper rectangle"""
        p1 = Point(2, 5)
        p2 = Point(9, 7)
        # Width = |9-2|+1 = 8, Height = |7-5|+1 = 3
        expected_area = 8 * 3
        self.assertEqual(p1.area(p2), expected_area)

    def test_point_area_from_example(self):
        """Test area calculations from problem example"""
        # Area 24 between 2,5 and 9,7
        p1 = Point(2, 5)
        p2 = Point(9, 7)
        self.assertEqual(p1.area(p2), 24)

        # Area 35 between 7,1 and 11,7
        p1 = Point(7, 1)
        p2 = Point(11, 7)
        self.assertEqual(p1.area(p2), 35)

        # Area 6 between 7,3 and 2,3
        p1 = Point(7, 3)
        p2 = Point(2, 3)
        self.assertEqual(p1.area(p2), 6)

        # Area 50 between 2,5 and 11,1
        p1 = Point(2, 5)
        p2 = Point(11, 1)
        self.assertEqual(p1.area(p2), 50)

    def test_point_area_negative_coords(self):
        """Test area with negative coordinates"""
        p1 = Point(-5, -3)
        p2 = Point(2, 4)
        # Width = |2-(-5)|+1 = 8, Height = |4-(-3)|+1 = 8
        self.assertEqual(p1.area(p2), 64)

    def test_point_area_single_width(self):
        """Test rectangle with width of 1"""
        p1 = Point(5, 3)
        p2 = Point(5, 7)
        # Width = 1, Height = 5
        self.assertEqual(p1.area(p2), 5)

    def test_point_area_unit_square(self):
        """Test 1x1 square (same point)"""
        p = Point(5, 5)
        self.assertEqual(p.area(p), 1)


class TestEdge(unittest.TestCase):
    """Test the Edge class"""

    def test_edge_creation(self):
        """Test basic edge creation"""
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        edge = Edge(p1, p2)
        self.assertEqual(edge.p, p1)
        self.assertEqual(edge.q, p2)

    def test_bounding_box_simple(self):
        """Test bounding box for simple edge"""
        edge = Edge(Point(0, 0), Point(3, 4))
        bbox = edge.bounding_box()
        self.assertEqual(bbox, ((0, 3), (0, 4)))

    def test_bounding_box_reversed(self):
        """Test bounding box when points are reversed"""
        edge = Edge(Point(3, 4), Point(0, 0))
        bbox = edge.bounding_box()
        self.assertEqual(bbox, ((0, 3), (0, 4)))

    def test_bounding_box_vertical(self):
        """Test bounding box for vertical edge"""
        edge = Edge(Point(5, 2), Point(5, 8))
        bbox = edge.bounding_box()
        self.assertEqual(bbox, ((5, 5), (2, 8)))

    def test_bounding_box_horizontal(self):
        """Test bounding box for horizontal edge"""
        edge = Edge(Point(2, 5), Point(8, 5))
        bbox = edge.bounding_box()
        self.assertEqual(bbox, ((2, 8), (5, 5)))

    def test_x_at_y_horizontal(self):
        """Test x_at_y for horizontal edge"""
        edge = Edge(Point(2, 5), Point(8, 5))
        # For horizontal edge, should return min x
        self.assertEqual(edge.x_at_y(5), 2)

    def test_x_at_y_vertical(self):
        """Test x_at_y for vertical edge"""
        edge = Edge(Point(5, 2), Point(5, 8))
        # For vertical edge, should return the x coordinate
        self.assertEqual(edge.x_at_y(4), 5)
        self.assertEqual(edge.x_at_y(7), 5)

    def test_x_at_y_diagonal(self):
        """Test x_at_y for diagonal edge"""
        # Edge from (0, 0) to (4, 4)
        edge = Edge(Point(0, 0), Point(4, 4))
        self.assertEqual(edge.x_at_y(0), 0)
        self.assertEqual(edge.x_at_y(2), 2)
        self.assertEqual(edge.x_at_y(4), 4)

    def test_x_at_y_general(self):
        """Test x_at_y for general edge"""
        # Edge from (0, 0) to (10, 5)
        edge = Edge(Point(0, 0), Point(10, 5))
        self.assertEqual(edge.x_at_y(0), 0)
        self.assertAlmostEqual(edge.x_at_y(2.5), 5)
        self.assertEqual(edge.x_at_y(5), 10)

    def test_collinear_on_line(self):
        """Test collinear for points on the line"""
        edge = Edge(Point(0, 0), Point(4, 4))
        self.assertTrue(edge.collinear(Point(0, 0)))
        self.assertTrue(edge.collinear(Point(4, 4)))
        self.assertTrue(edge.collinear(Point(2, 2)))

    def test_collinear_off_line(self):
        """Test collinear for points off the line"""
        edge = Edge(Point(0, 0), Point(4, 4))
        self.assertFalse(edge.collinear(Point(0, 1)))
        self.assertFalse(edge.collinear(Point(1, 0)))
        self.assertFalse(edge.collinear(Point(3, 2)))

    def test_collinear_horizontal(self):
        """Test collinear for horizontal edge"""
        edge = Edge(Point(0, 5), Point(10, 5))
        self.assertTrue(edge.collinear(Point(5, 5)))
        self.assertFalse(edge.collinear(Point(5, 6)))

    def test_collinear_vertical(self):
        """Test collinear for vertical edge"""
        edge = Edge(Point(5, 0), Point(5, 10))
        self.assertTrue(edge.collinear(Point(5, 5)))
        self.assertFalse(edge.collinear(Point(6, 5)))

    def test_collinear_extended_line(self):
        """Test collinear for points on extended line but outside segment"""
        edge = Edge(Point(2, 2), Point(4, 4))

        # On the line, within segment
        self.assertTrue(edge.collinear(Point(3, 3)))

        # On the line, but extended beyond
        self.assertTrue(edge.collinear(Point(0, 0)))  # Before start
        self.assertTrue(edge.collinear(Point(6, 6)))  # After end


class TestPolygon(unittest.TestCase):
    """Test the Polygon class"""

    def test_polygon_creation_triangle(self):
        """Test creating a simple triangle"""
        points = [Point(0, 0), Point(4, 0), Point(2, 3)]
        poly = Polygon(points)
        self.assertEqual(len(poly.points), 3)
        self.assertEqual(len(poly.edges), 3)

    def test_polygon_creation_square(self):
        """Test creating a square"""
        points = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
        poly = Polygon(points)
        self.assertEqual(len(poly.points), 4)
        self.assertEqual(len(poly.edges), 4)

    def test_polygon_bounds_square(self):
        """Test polygon bounds for a square"""
        points = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
        poly = Polygon(points)
        self.assertEqual(poly.min_x, 0)
        self.assertEqual(poly.max_x, 4)
        self.assertEqual(poly.min_y, 0)
        self.assertEqual(poly.max_y, 4)

    def test_outside_square_clearly_inside(self):
        """Test points clearly inside a square"""
        points = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
        poly = Polygon(points)

        self.assertFalse(poly.outside(Point(5, 5)))
        self.assertFalse(poly.outside(Point(1, 1)))
        self.assertFalse(poly.outside(Point(9, 9)))

    def test_outside_square_clearly_outside(self):
        """Test points clearly outside a square"""
        points = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
        poly = Polygon(points)

        self.assertTrue(poly.outside(Point(-1, 5)))
        self.assertTrue(poly.outside(Point(11, 5)))
        self.assertTrue(poly.outside(Point(5, -1)))
        self.assertTrue(poly.outside(Point(5, 11)))
        self.assertTrue(poly.outside(Point(15, 15)))

    def test_outside_square_on_edge(self):
        """Test points on the edge of a square"""
        points = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
        poly = Polygon(points)

        # Points on edges should be considered inside (not outside)
        self.assertFalse(poly.outside(Point(0, 5)))
        self.assertFalse(poly.outside(Point(10, 5)))
        self.assertFalse(poly.outside(Point(5, 0)))
        self.assertFalse(poly.outside(Point(5, 10)))

    def test_outside_square_on_vertex(self):
        """Test points at vertices of a square"""
        points = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]
        poly = Polygon(points)

        # Vertices should be considered inside (not outside)
        self.assertFalse(poly.outside(Point(0, 0)))
        self.assertFalse(poly.outside(Point(10, 0)))
        self.assertFalse(poly.outside(Point(10, 10)))
        self.assertFalse(poly.outside(Point(0, 10)))

    def test_outside_triangle_inside(self):
        """Test points inside a triangle"""
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        poly = Polygon(points)

        self.assertFalse(poly.outside(Point(5, 5)))
        self.assertFalse(poly.outside(Point(3, 3)))
        self.assertFalse(poly.outside(Point(7, 3)))

    def test_outside_triangle_outside(self):
        """Test points outside a triangle"""
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        poly = Polygon(points)

        self.assertTrue(poly.outside(Point(0, 5)))
        self.assertTrue(poly.outside(Point(10, 5)))
        self.assertTrue(poly.outside(Point(5, 15)))

    def test_outside_concave_polygon(self):
        """Test with a concave polygon (L-shape)"""
        # L-shaped polygon
        points = [
            Point(0, 0), Point(5, 0), Point(5, 5),
            Point(2, 5), Point(2, 2), Point(0, 2)
        ]
        poly = Polygon(points)

        # Inside the L
        self.assertFalse(poly.outside(Point(1, 1)))
        self.assertFalse(poly.outside(Point(3, 3)))

        # In the concave part (should be outside)
        self.assertTrue(poly.outside(Point(1, 4)))

        # Clearly outside
        self.assertTrue(poly.outside(Point(6, 6)))
        self.assertTrue(poly.outside(Point(-1, -1)))

    def test_outside_example_polygon(self):
        """Test with the example from the problem"""
        points = [
            Point(7, 1),
            Point(11, 1),
            Point(11, 7),
            Point(9, 7),
            Point(9, 5),
            Point(2, 5),
            Point(2, 3),
            Point(7, 3),
        ]
        poly = Polygon(points)

        # Test the corners that should work (from part 2 example)
        # Rectangle between 9,5 and 2,3 with area 24 should work
        p1 = Point(9, 5)
        p2 = Point(2, 3)
        # Check the other two corners: (9, 3) and (2, 5)
        self.assertFalse(poly.outside(Point(9, 3)))
        self.assertFalse(poly.outside(Point(2, 5)))

        # Points clearly outside the polygon
        self.assertTrue(poly.outside(Point(0, 0)))
        self.assertTrue(poly.outside(Point(15, 15)))

    def test_outside_ray_through_vertex(self):
        """Test point where ray passes through a vertex"""
        # Diamond shape
        points = [Point(5, 0), Point(10, 5), Point(5, 10), Point(0, 5)]
        poly = Polygon(points)

        # Point at y=5 shoots ray through vertices at (0,5) and (10,5)
        self.assertFalse(poly.outside(Point(5, 5)))  # Center should be inside
        self.assertTrue(poly.outside(Point(-1, 5)))  # Left should be outside
        self.assertTrue(poly.outside(Point(11, 5)))  # Right should be outside

    def test_outside_negative_coords(self):
        """Test polygon with negative coordinates"""
        points = [Point(-5, -5), Point(5, -5), Point(5, 5), Point(-5, 5)]
        poly = Polygon(points)

        self.assertFalse(poly.outside(Point(0, 0)))
        self.assertTrue(poly.outside(Point(-10, 0)))
        self.assertTrue(poly.outside(Point(10, 0)))

    def test_outside_counter_clockwise(self):
        """Test polygon with counter-clockwise winding"""
        # Counter-clockwise square
        points = [Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0)]
        poly = Polygon(points)

        self.assertFalse(poly.outside(Point(5, 5)))
        self.assertTrue(poly.outside(Point(15, 15)))

    def test_outside_multiple_horizontal_edges(self):
        """Test polygon with multiple horizontal edges at different y values"""
        # Rectangle with a notch cut out
        points = [
            Point(0, 0), Point(10, 0), Point(10, 10),
            Point(6, 10), Point(6, 5), Point(4, 5),
            Point(4, 10), Point(0, 10)
        ]
        poly = Polygon(points)

        # Inside the notch
        self.assertTrue(poly.outside(Point(5, 7)))
        # Inside the main rectangle
        self.assertFalse(poly.outside(Point(2, 5)))
        # Definitely outside
        self.assertTrue(poly.outside(Point(12, 5)))


class TestGetInputs(unittest.TestCase):
    """Test input parsing"""

    def test_get_inputs_simple(self):
        """Test parsing simple input"""
        input_str = "1,2\n3,4\n5,6\n"
        points = get_inputs(StringIO(input_str))
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0], Point(1, 2))
        self.assertEqual(points[1], Point(3, 4))
        self.assertEqual(points[2], Point(5, 6))

    def test_get_inputs_with_empty_lines(self):
        """Test parsing input with empty lines"""
        input_str = "1,2\n\n3,4\n\n\n5,6\n"
        points = get_inputs(StringIO(input_str))
        self.assertEqual(len(points), 3)

    def test_get_inputs_example(self):
        """Test parsing the example input"""
        input_str = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
        points = get_inputs(StringIO(input_str))
        self.assertEqual(len(points), 8)
        self.assertEqual(points[0], Point(7, 1))
        self.assertEqual(points[-1], Point(7, 3))

    def test_get_inputs_invalid_coords(self):
        """Test that invalid input raises ValueError"""
        input_str = "1,2,3\n"  # Too many coordinates
        with self.assertRaises(ValueError):
            get_inputs(StringIO(input_str))

    def test_get_inputs_single_point(self):
        """Test parsing a single point"""
        input_str = "5,7\n"
        points = get_inputs(StringIO(input_str))
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0], Point(5, 7))


class TestFullExample(unittest.TestCase):
    """Test the full example from the problem"""

    def setUp(self):
        """Set up the example points"""
        self.points = [
            Point(7, 1),
            Point(11, 1),
            Point(11, 7),
            Point(9, 7),
            Point(9, 5),
            Point(2, 5),
            Point(2, 3),
            Point(7, 3),
        ]

    def test_part1_max_area(self):
        """Test that part 1 finds the maximum area of 50"""
        max_area = 0
        for i, p in enumerate(self.points):
            for j, q in enumerate(self.points):
                if i <= j:
                    continue
                max_area = max(p.area(q), max_area)

        self.assertEqual(max_area, 50)

    def test_part1_specific_areas(self):
        """Test specific rectangle areas from part 1"""
        # Area 24 between indices for 2,5 and 9,7
        p1 = Point(2, 5)
        p2 = Point(9, 7)
        self.assertEqual(p1.area(p2), 24)

        # Area 35 between 7,1 and 11,7
        p1 = Point(7, 1)
        p2 = Point(11, 7)
        self.assertEqual(p1.area(p2), 35)

    def test_part2_max_area(self):
        """Test that part 2 finds the maximum area of 24"""
        max_area = 0
        poly = Polygon(self.points)

        for i, p in enumerate(self.points):
            for j, q in enumerate(self.points):
                if i <= j:
                    continue
                # Check if the other two corners are inside the polygon
                if poly.outside(Point(p.x, q.y)):
                    continue
                if poly.outside(Point(q.x, p.y)):
                    continue
                max_area = max(p.area(q), max_area)

        self.assertEqual(max_area, 24)

    def test_part2_specific_invalid_rectangles(self):
        """Test that certain rectangles are correctly rejected in part 2"""
        poly = Polygon(self.points)

        # The rectangle with area 50 from part 1 should not work in part 2
        # because its corners extend outside the polygon
        p1 = Point(2, 5)
        p2 = Point(11, 1)
        # Check if corners (2, 1) or (11, 5) are outside
        corner1_inside = not poly.outside(Point(p1.x, p2.y))
        corner2_inside = not poly.outside(Point(p2.x, p1.y))

        # At least one should be outside
        self.assertFalse(corner1_inside and corner2_inside)


if __name__ == '__main__':
    unittest.main()
