#!/usr/bin/env python3
import unittest
from io import StringIO
from day11 import Edge, DirectedGraph, get_inputs


class TestEdge(unittest.TestCase):
    """Test the Edge dataclass."""

    def test_edge_creation(self):
        edge = Edge("a", "b")
        self.assertEqual(edge.start, "a")
        self.assertEqual(edge.end, "b")

    def test_edge_equality(self):
        edge1 = Edge("a", "b")
        edge2 = Edge("a", "b")
        self.assertEqual(edge1, edge2)

    def test_edge_ordering(self):
        edge1 = Edge("a", "b")
        edge2 = Edge("b", "c")
        self.assertLess(edge1, edge2)


class TestGetInputs(unittest.TestCase):
    """Test the input parsing function."""

    def test_parse_simple_input(self):
        input_text = "aaa: bbb ccc\n"
        edges = get_inputs(StringIO(input_text))
        self.assertEqual(len(edges), 2)
        self.assertIn(Edge("aaa", "bbb"), edges)
        self.assertIn(Edge("aaa", "ccc"), edges)

    def test_parse_example_input(self):
        input_text = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
        edges = get_inputs(StringIO(input_text))
        # Count expected edges: 2+2+2+3+1+1+1+1+3+1 = 17
        self.assertEqual(len(edges), 17)
        self.assertIn(Edge("you", "bbb"), edges)
        self.assertIn(Edge("you", "ccc"), edges)

    def test_parse_empty_lines_ignored(self):
        input_text = "aaa: bbb\n\nbbb: ccc\n\n"
        edges = get_inputs(StringIO(input_text))
        self.assertEqual(len(edges), 2)

    def test_parse_single_destination(self):
        input_text = "aaa: bbb\n"
        edges = get_inputs(StringIO(input_text))
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0], Edge("aaa", "bbb"))


class TestDirectedGraph(unittest.TestCase):
    """Test the DirectedGraph class."""

    def test_graph_construction(self):
        edges = [Edge("a", "b"), Edge("b", "c")]
        graph = DirectedGraph(edges)
        self.assertIn("a", graph.nodes)
        self.assertIn("b", graph.nodes)
        self.assertIn("c", graph.nodes)
        self.assertEqual(graph.adjacencies["a"], ["b"])
        self.assertEqual(graph.adjacencies["b"], ["c"])

    def test_graph_with_multiple_destinations(self):
        edges = [Edge("a", "b"), Edge("a", "c")]
        graph = DirectedGraph(edges)
        self.assertEqual(set(graph.adjacencies["a"]), {"b", "c"})


class TestAllPaths(unittest.TestCase):
    """Test the all_paths method with various scenarios."""

    def test_example_from_problem(self):
        """Test the example from the problem description (should find 5 paths)."""
        input_text = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
        edges = get_inputs(StringIO(input_text))
        graph = DirectedGraph(edges)
        paths = graph.all_paths("you", "out")

        # Expected paths from problem description:
        # 1. you -> bbb -> ddd -> ggg -> out
        # 2. you -> bbb -> eee -> out
        # 3. you -> ccc -> ddd -> ggg -> out
        # 4. you -> ccc -> eee -> out
        # 5. you -> ccc -> fff -> out
        self.assertEqual(len(paths), 5)

        # Verify each expected path exists
        expected_paths = [
            ["you", "bbb", "ddd", "ggg", "out"],
            ["you", "bbb", "eee", "out"],
            ["you", "ccc", "ddd", "ggg", "out"],
            ["you", "ccc", "eee", "out"],
            ["you", "ccc", "fff", "out"],
        ]
        for expected_path in expected_paths:
            self.assertIn(expected_path, paths)

    def test_simple_linear_path(self):
        """Test a simple linear path: a -> b -> c."""
        edges = [Edge("a", "b"), Edge("b", "c")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "c")
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], ["a", "b", "c"])

    def test_single_hop(self):
        """Test a direct connection: a -> b."""
        edges = [Edge("a", "b")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "b")
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], ["a", "b"])

    def test_no_path_exists(self):
        """Test when there's no path from source to destination."""
        edges = [Edge("a", "b"), Edge("c", "d")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "d")
        self.assertEqual(len(paths), 0)

    def test_multiple_paths_different_lengths(self):
        """Test finding multiple paths of different lengths."""
        # a -> b -> d
        # a -> c -> d
        edges = [Edge("a", "b"), Edge("a", "c"), Edge("b", "d"), Edge("c", "d")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "d")
        self.assertEqual(len(paths), 2)
        self.assertIn(["a", "b", "d"], paths)
        self.assertIn(["a", "c", "d"], paths)

    def test_cycle_avoidance(self):
        """Test that cycles are properly avoided."""
        # a -> b -> c -> a (cycle)
        # a -> d
        edges = [Edge("a", "b"), Edge("b", "c"), Edge("c", "a"), Edge("a", "d")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "d")
        # Should only find one path: a -> d
        # The cycle should not cause infinite loops
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], ["a", "d"])

    def test_source_equals_destination(self):
        """Test when source and destination are the same."""
        edges = [Edge("a", "b")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "a")
        # Should return path with just the source node
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], ["a"])

    def test_complex_graph_with_many_paths(self):
        """Test a more complex graph with multiple overlapping paths."""
        # Diamond pattern with extra connections
        #     a
        #    / \
        #   b   c
        #   |\ /|
        #   | X |
        #   |/ \|
        #   d   e
        #    \ /
        #     f
        edges = [
            Edge("a", "b"), Edge("a", "c"),
            Edge("b", "d"), Edge("b", "e"),
            Edge("c", "d"), Edge("c", "e"),
            Edge("d", "f"), Edge("e", "f")
        ]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "f")
        # Expected paths:
        # a -> b -> d -> f
        # a -> b -> e -> f
        # a -> c -> d -> f
        # a -> c -> e -> f
        self.assertEqual(len(paths), 4)

    def test_disconnected_destination(self):
        """Test when destination node exists but is unreachable."""
        edges = [Edge("a", "b"), Edge("c", "d"), Edge("d", "out")]
        graph = DirectedGraph(edges)
        paths = graph.all_paths("a", "out")
        self.assertEqual(len(paths), 0)

    def test_node_with_no_outgoing_edges(self):
        """Test path ending at a node with no outgoing edges."""
        edges = [Edge("a", "b"), Edge("b", "c")]
        graph = DirectedGraph(edges)
        # Node "c" has no outgoing edges
        paths = graph.all_paths("a", "c")
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], ["a", "b", "c"])


class TestCountPaths(unittest.TestCase):
    """Test the count_paths method (optimized counting without storing paths)."""

    def test_count_matches_all_paths_length(self):
        """Verify count_paths gives same result as len(all_paths)."""
        input_text = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
        edges = get_inputs(StringIO(input_text))
        graph = DirectedGraph(edges)

        all_paths = graph.all_paths("you", "out")
        count = graph.count_paths("you", "out")

        self.assertEqual(count, len(all_paths))

    def test_count_with_avoid(self):
        """Test counting paths with avoid list."""
        edges = [
            Edge("a", "b"), Edge("a", "c"),
            Edge("b", "d"), Edge("c", "d"),
            Edge("b", "x"), Edge("x", "d")
        ]
        graph = DirectedGraph(edges)

        # Without avoid: 3 paths (a->b->d, a->c->d, a->b->x->d)
        self.assertEqual(graph.count_paths("a", "d"), 3)

        # Avoiding x: 2 paths (a->b->d, a->c->d)
        self.assertEqual(graph.count_paths("a", "d", avoid=["x"]), 2)

    def test_count_no_paths(self):
        """Test counting when no paths exist."""
        edges = [Edge("a", "b"), Edge("c", "d")]
        graph = DirectedGraph(edges)
        self.assertEqual(graph.count_paths("a", "d"), 0)


if __name__ == "__main__":
    unittest.main()
