#!/usr/bin/env python3
"""
Test suite for Advent of Code 2025 - Day 8: Wiring neighbouring junctions
"""
import unittest
import io
from day08 import Point, UnionFind, get_inputs, nearest_n_neighbours, connected_circuits


class TestPoint(unittest.TestCase):
    """Test cases for the Point class"""

    def test_point_creation(self):
        """Test that points can be created with correct coordinates"""
        p = Point(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)

    def test_point_ordering(self):
        """Test that points can be ordered (for use in sorted structures)"""
        p1 = Point(1, 2, 3)
        p2 = Point(1, 2, 4)
        p3 = Point(2, 1, 1)
        self.assertLess(p1, p2)
        self.assertLess(p1, p3)

    def test_point_frozen(self):
        """Test that points are immutable (frozen)"""
        p = Point(1, 2, 3)
        with self.assertRaises(AttributeError):
            p.x = 5

    def test_dist_sq_same_point(self):
        """Test squared distance from a point to itself is 0"""
        p = Point(5, 10, 15)
        self.assertEqual(p.dist_sq(p), 0)

    def test_dist_sq_simple(self):
        """Test squared distance calculation with simple values"""
        p1 = Point(0, 0, 0)
        p2 = Point(3, 4, 0)
        # 3^2 + 4^2 + 0^2 = 9 + 16 = 25
        self.assertEqual(p1.dist_sq(p2), 25)

    def test_dist_sq_3d(self):
        """Test squared distance calculation in 3D"""
        p1 = Point(1, 2, 3)
        p2 = Point(4, 6, 8)
        # (4-1)^2 + (6-2)^2 + (8-3)^2 = 9 + 16 + 25 = 50
        self.assertEqual(p1.dist_sq(p2), 50)

    def test_dist_sq_symmetric(self):
        """Test that distance is symmetric (dist(p,q) == dist(q,p))"""
        p1 = Point(10, 20, 30)
        p2 = Point(40, 50, 60)
        self.assertEqual(p1.dist_sq(p2), p2.dist_sq(p1))

    def test_str_formatting(self):
        """Test string representation of points"""
        p = Point(162, 817, 812)
        s = str(p)
        # Should contain the coordinates
        self.assertIn("162", s)
        self.assertIn("817", s)
        self.assertIn("812", s)


class TestUnionFind(unittest.TestCase):
    """Test cases for the UnionFind class"""

    def test_initialization(self):
        """Test that UnionFind initializes correctly"""
        uf = UnionFind(5)
        # Initially, each element is its own parent
        for i in range(5):
            self.assertEqual(uf.find(i), i)

    def test_find_self(self):
        """Test finding root of isolated elements"""
        uf = UnionFind(3)
        self.assertEqual(uf.find(0), 0)
        self.assertEqual(uf.find(1), 1)
        self.assertEqual(uf.find(2), 2)

    def test_union_simple(self):
        """Test simple union of two elements"""
        uf = UnionFind(3)
        uf.union(0, 1)
        # After union, 0 and 1 should have the same root
        self.assertEqual(uf.find(0), uf.find(1))
        # But 2 should still be separate
        self.assertNotEqual(uf.find(2), uf.find(0))

    def test_connected_after_union(self):
        """Test that connected() returns True after union"""
        uf = UnionFind(5)
        self.assertFalse(uf.connected(0, 1))
        uf.union(0, 1)
        self.assertTrue(uf.connected(0, 1))
        self.assertTrue(uf.connected(1, 0))  # symmetric

    def test_connected_transitive(self):
        """Test transitive connectivity: if 0-1 and 1-2, then 0-2"""
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        self.assertTrue(uf.connected(0, 2))
        self.assertTrue(uf.connected(2, 0))

    def test_multiple_unions(self):
        """Test multiple unions creating separate components"""
        uf = UnionFind(6)
        uf.union(0, 1)
        uf.union(1, 2)  # Component: {0, 1, 2}
        uf.union(3, 4)  # Component: {3, 4}
        # Element 5 remains alone

        self.assertTrue(uf.connected(0, 2))
        self.assertTrue(uf.connected(3, 4))
        self.assertFalse(uf.connected(0, 3))
        self.assertFalse(uf.connected(0, 5))
        self.assertFalse(uf.connected(3, 5))

    def test_path_compression(self):
        """Test that path compression works (indirect test via performance)"""
        uf = UnionFind(100)
        # Create a long chain
        for i in range(99):
            uf.union(i, i + 1)
        # After finding, path should be compressed
        root1 = uf.find(0)
        root2 = uf.find(99)
        self.assertEqual(root1, root2)


class TestGetInputs(unittest.TestCase):
    """Test cases for the get_inputs function"""

    def test_simple_input(self):
        """Test parsing simple valid input"""
        input_str = "1,2,3\n4,5,6\n"
        fileobj = io.StringIO(input_str)
        points = get_inputs(fileobj)

        self.assertEqual(len(points), 2)
        self.assertEqual(points[0], Point(1, 2, 3))
        self.assertEqual(points[1], Point(4, 5, 6))

    def test_empty_lines_ignored(self):
        """Test that empty lines are ignored"""
        input_str = "1,2,3\n\n4,5,6\n\n"
        fileobj = io.StringIO(input_str)
        points = get_inputs(fileobj)

        self.assertEqual(len(points), 2)

    def test_large_coordinates(self):
        """Test parsing large coordinate values"""
        input_str = "162,817,812\n906,360,560\n"
        fileobj = io.StringIO(input_str)
        points = get_inputs(fileobj)

        self.assertEqual(len(points), 2)
        self.assertEqual(points[0], Point(162, 817, 812))
        self.assertEqual(points[1], Point(906, 360, 560))

    def test_invalid_coordinates_raises_error(self):
        """Test that invalid number of coordinates raises ValueError"""
        input_str = "1,2\n"  # Only 2 coordinates instead of 3
        fileobj = io.StringIO(input_str)

        with self.assertRaises(ValueError) as cm:
            get_inputs(fileobj)
        self.assertIn("Invalid number of coordinates", str(cm.exception))

    def test_too_many_coordinates_raises_error(self):
        """Test that too many coordinates raises ValueError"""
        input_str = "1,2,3,4\n"  # 4 coordinates instead of 3
        fileobj = io.StringIO(input_str)

        with self.assertRaises(ValueError) as cm:
            get_inputs(fileobj)
        self.assertIn("Invalid number of coordinates", str(cm.exception))


class TestNearestNNeighbours(unittest.TestCase):
    """Test cases for the nearest_n_neighbours function"""

    def test_two_points(self):
        """Test finding nearest neighbor with just two points"""
        points = [Point(0, 0, 0), Point(1, 0, 0)]
        neighbours = nearest_n_neighbours(points, 1)

        self.assertEqual(len(neighbours), 1)
        dist_sq, (i, j) = neighbours[0]
        self.assertEqual(dist_sq, 1)
        self.assertEqual((i, j), (1, 0))

    def test_three_points_sorted(self):
        """Test that results are sorted by distance"""
        points = [
            Point(0, 0, 0),
            Point(10, 0, 0),
            Point(1, 0, 0)
        ]
        neighbours = nearest_n_neighbours(points, 2)

        self.assertEqual(len(neighbours), 2)
        # Closest should be (0,0,0) to (1,0,0) with dist_sq = 1
        self.assertEqual(neighbours[0][0], 1)
        # Next closest should be (1,0,0) to (10,0,0) with dist_sq = 81
        self.assertEqual(neighbours[1][0], 81)

    def test_limits_to_n(self):
        """Test that only n nearest pairs are returned"""
        points = [Point(i, 0, 0) for i in range(10)]
        n = 5
        neighbours = nearest_n_neighbours(points, n)

        self.assertEqual(len(neighbours), n)

    def test_all_pairs_when_n_none(self):
        """Test that all pairs are returned when n is None"""
        points = [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0)]
        # With 3 points, there are C(3,2) = 3 pairs
        neighbours = nearest_n_neighbours(points, None)

        self.assertEqual(len(neighbours), 3)

    def test_example_closest_pair(self):
        """Test finding the closest pair from the problem example"""
        points = [
            Point(162, 817, 812),
            Point(425, 690, 689)
        ]
        neighbours = nearest_n_neighbours(points, 1)

        self.assertEqual(len(neighbours), 1)
        # Calculate expected distance: (425-162)^2 + (690-817)^2 + (689-812)^2
        # = 263^2 + (-127)^2 + (-123)^2 = 69169 + 16129 + 15129 = 100427
        expected_dist_sq = 263**2 + 127**2 + 123**2
        self.assertEqual(neighbours[0][0], expected_dist_sq)


class TestConnectedCircuits(unittest.TestCase):
    """Test cases for the connected_circuits function"""

    def test_single_point_no_edges(self):
        """Test single point with no edges"""
        points = [Point(0, 0, 0)]
        edges = []
        circuits = connected_circuits(points, edges)

        self.assertEqual(len(circuits), 1)
        self.assertEqual(len(circuits[0]), 1)

    def test_two_points_connected(self):
        """Test two points connected by an edge"""
        points = [Point(0, 0, 0), Point(1, 0, 0)]
        edges = [(1, (0, 1))]
        circuits = connected_circuits(points, edges)

        self.assertEqual(len(circuits), 1)
        self.assertEqual(len(circuits[0]), 2)

    def test_two_points_not_connected(self):
        """Test two points with no connecting edge"""
        points = [Point(0, 0, 0), Point(1, 0, 0)]
        edges = []
        circuits = connected_circuits(points, edges)

        self.assertEqual(len(circuits), 2)
        self.assertTrue(all(len(c) == 1 for c in circuits))

    def test_chain_of_connections(self):
        """Test chain: 0-1-2-3 all connected"""
        points = [Point(i, 0, 0) for i in range(4)]
        edges = [
            (1, (0, 1)),
            (1, (1, 2)),
            (1, (2, 3))
        ]
        circuits = connected_circuits(points, edges)

        self.assertEqual(len(circuits), 1)
        self.assertEqual(len(circuits[0]), 4)

    def test_multiple_separate_circuits(self):
        """Test multiple separate circuits"""
        points = [Point(i, 0, 0) for i in range(6)]
        edges = [
            (1, (0, 1)),  # Circuit 1: {0, 1}
            (1, (2, 3)),  # Circuit 2: {2, 3}
            (1, (3, 4))   # Extends circuit 2: {2, 3, 4}
        ]
        # Result should be: {0,1}, {2,3,4}, {5}
        circuits = connected_circuits(points, edges)

        self.assertEqual(len(circuits), 3)
        circuit_sizes = sorted([len(c) for c in circuits])
        self.assertEqual(circuit_sizes, [1, 2, 3])


class TestFullExample(unittest.TestCase):
    """Test the complete example from the problem statement"""

    def setUp(self):
        """Set up the 20 junction boxes from the problem example"""
        coords = [
            (162, 817, 812),
            (57, 618, 57),
            (906, 360, 560),
            (592, 479, 940),
            (352, 342, 300),
            (466, 668, 158),
            (542, 29, 236),
            (431, 825, 988),
            (739, 650, 466),
            (52, 470, 668),
            (216, 146, 977),
            (819, 987, 18),
            (117, 168, 530),
            (805, 96, 715),
            (346, 949, 466),
            (970, 615, 88),
            (941, 993, 340),
            (862, 61, 35),
            (984, 92, 344),
            (425, 690, 689)
        ]
        self.example_points = [Point(x, y, z) for x, y, z in coords]

    def test_example_closest_pair(self):
        """Test that the closest pair is 162,817,812 and 425,690,689"""
        neighbours = nearest_n_neighbours(self.example_points, 1)

        dist_sq, (i, j) = neighbours[0]

        # The closest pair should be points at indices 0 and 19
        point_i = self.example_points[i]
        point_j = self.example_points[j]

        # One should be 162,817,812 and the other 425,690,689
        self.assertTrue(
            (point_i == Point(162, 817, 812) and point_j == Point(425, 690, 689)) or
            (point_i == Point(425, 690, 689) and point_j == Point(162, 817, 812))
        )

    def test_example_ten_connections(self):
        """Test the example with 10 connections as specified in the problem"""
        neighbours = nearest_n_neighbours(self.example_points, 10)
        circuits = connected_circuits(self.example_points, neighbours)

        # After 10 connections, there should be 11 circuits
        # (20 points - 10 connections + number_of_cycles, but if no cycles: 20 - 10 = 10...
        # Actually the problem says 11 circuits)
        # Let me re-read: "After making the ten shortest connections, there are 11 circuits"
        self.assertEqual(len(circuits), 11)

    def test_example_circuit_sizes(self):
        """Test that circuit sizes match the problem description after 10 connections"""
        neighbours = nearest_n_neighbours(self.example_points, 10)
        circuits = connected_circuits(self.example_points, neighbours)

        circuit_sizes = sorted([len(c) for c in circuits])

        # The problem states:
        # - one circuit with 5 junction boxes
        # - one circuit with 4 junction boxes
        # - two circuits with 2 junction boxes each
        # - seven circuits with 1 junction box each
        expected_sizes = [1, 1, 1, 1, 1, 1, 1, 2, 2, 4, 5]
        self.assertEqual(circuit_sizes, expected_sizes)

    def test_example_result(self):
        """Test that the final result matches the expected answer of 40"""
        neighbours = nearest_n_neighbours(self.example_points, 10)
        circuits = connected_circuits(self.example_points, neighbours)

        circuit_sizes = sorted([len(c) for c in circuits])
        # Multiply the three largest: 5 * 4 * 2 = 40
        result = circuit_sizes[-1] * circuit_sizes[-2] * circuit_sizes[-3]

        self.assertEqual(result, 40)


if __name__ == "__main__":
    unittest.main()
