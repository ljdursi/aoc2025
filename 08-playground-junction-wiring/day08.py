#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 8: Wiring neighbouring junctions
"""
import argparse
import sys
from typing import TextIO
from dataclasses import dataclass
import bisect
import functools
import operator


@dataclass(order=True, frozen=True)
class Point:
    """Represents a point in 3D space with integer coordinates."""
    x: int
    y: int
    z: int

    def dist_sq(self, q: "Point") -> int:
        """Calculate the squared Euclidean distance to another point.

        Args:
            q: The other point

        Returns:
            The squared distance (avoids floating point operations)
        """
        return (self.x - q.x)**2 + (self.y - q.y)**2 + (self.z - q.z)**2

    def __str__(self) -> str:
        """Format point as comma-separated coordinates with fixed width."""
        return f"{self.x:>5},{self.y:>5},{self.z:>5}"


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure with path compression and union by rank.

    Efficiently tracks connected components, supporting near-constant time operations
    for finding component membership and merging components.
    """

    def __init__(self, size: int):
        """Initialize Union-Find structure with size isolated elements.

        Args:
            size: Number of elements (0 to size-1)
        """
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p: int) -> int:
        """Find the root representative of the component containing p.

        Uses path compression to flatten the tree structure for future operations.

        Args:
            p: Element to find root of

        Returns:
            The root of p's component
        """
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p: int, q: int) -> None:
        """Merge the components containing p and q.

        Uses union by rank to keep trees balanced.

        Args:
            p: First element
            q: Second element
        """
        root_p = self.find(p)
        root_q = self.find(q)

        if root_p != root_q:
            # Union by rank
            if self.rank[root_p] > self.rank[root_q]:
                self.parent[root_q] = root_p
            elif self.rank[root_p] < self.rank[root_q]:
                self.parent[root_p] = root_q
            else:
                self.parent[root_q] = root_p
                self.rank[root_p] += 1

    def connected(self, p: int, q: int) -> bool:
        """Check if p and q are in the same component.

        Args:
            p: First element
            q: Second element

        Returns:
            True if p and q are connected
        """
        return self.find(p) == self.find(q)


def get_inputs(fileobj: TextIO) -> list[Point]:
    """Parse junction box positions from input file.

    Each line should contain three comma-separated integers (x,y,z).
    Empty lines are ignored.

    Args:
        fileobj: Input file object

    Returns:
        List of Point objects

    Raises:
        ValueError: If any line doesn't have exactly 3 coordinates
    """
    lines = [line.rstrip('\n') for line in fileobj.readlines() if line.strip()]

    line_ints = [[int(item) for item in line.split(',')] for line in lines]
    if not all(len(item) == 3 for item in line_ints):
        raise ValueError("Invalid number of coordinates in a point")

    return [Point(*item) for item in line_ints]


def nearest_n_neighbours(points: list[Point], n: int = None) -> list[tuple[int, tuple[int, int]]]:
    """Find the n pairs of points with smallest distances.

    Uses a bounded insertion algorithm to avoid computing and sorting all O(n²) pairs.
    Maintains a sorted list of the n smallest distances seen so far.

    Args:
        points: List of points to find nearest neighbors among
        n: Number of closest pairs to return (if None, returns all pairs)

    Returns:
        List of (distance_squared, (index_i, index_j)) tuples, sorted by distance.
        Indices satisfy i > j (each pair appears once).
    """
    n_points = len(points)
    if n is None:
        # Total number of unique pairs
        n = n_points * (n_points - 1) // 2

    # Initialize with sentinel values larger than any real distance
    distances: list[tuple[int, tuple[int, int]]] = [(sys.maxsize, (-1, -1))] * n

    def insert_into_list(dist_sq: int, start: int, end: int) -> None:
        """Insert a distance into the sorted list if it's small enough.

        Maintains exactly n elements by removing the largest when inserting.
        """
        newpt = (dist_sq, (start, end))

        # Skip if larger than our current largest
        if dist_sq > distances[-1][0]:
            return

        # Fast path: new smallest element
        if dist_sq < distances[0][0]:
            distances[:] = [newpt] + distances[:-1]
            return

        # Binary search for insertion point
        idx = bisect.bisect_left(distances, newpt)
        if idx >= len(distances):
            return
        # Insert at idx and drop the last (largest) element
        distances[:] = distances[0:idx] + [newpt] + distances[idx:-1]

    # Compute all pairwise distances
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if i <= j:
                continue
            dist_sq = p.dist_sq(q)
            insert_into_list(dist_sq, i, j)

    return distances


def connected_circuits(points: list[Point], distance_edges: list[tuple[int, tuple[int, int]]]) -> list[list[int]]:
    """Build connected circuits from a list of edges.

    Uses Union-Find to efficiently track which points are connected as edges are added.

    Args:
        points: List of all points
        distance_edges: List of (distance, (i, j)) tuples representing edges to add

    Returns:
        List of circuits, where each circuit is a list of point indices
    """
    n_points = len(points)

    uf = UnionFind(n_points)
    for _, (i, j) in distance_edges:
        uf.union(i, j)

    # Group points by their root component
    circuits: dict[int, list[int]] = {}
    for i in range(n_points):
        root = uf.find(i)
        if root not in circuits:
            circuits[root] = [i]
        else:
            circuits[root].append(i)

    return list(circuits.values())


def main() -> None:
    """Main entry point for the playground junction box wirer."""
    parser = argparse.ArgumentParser(
        prog='day08',
        description="Advent of Code 2025 - Day 8: Wiring the playground junction boxes"
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType('r'),
        help="Input file containing junction box positions (x,y,z coordinates)"
    )
    parser.add_argument(
        "n_connections",
        type=int,
        nargs='?',
        default=10,
        help="Number of connections to make (default: 10)"
    )
    args = parser.parse_args()

    points = get_inputs(args.input_file)
    neighbours = nearest_n_neighbours(points, args.n_connections)

    print("Part 1")
    circuits = connected_circuits(points, neighbours)
    circuit_lengths = sorted([len(c) for c in circuits])
    result = functools.reduce(operator.mul, circuit_lengths[-3:])
    print(result)


if __name__ == "__main__":
    main()
