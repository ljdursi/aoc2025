#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 8: Wiring neighbouring junctions
"""
import argparse
from typing import TextIO
from dataclasses import dataclass
from collections import defaultdict
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


class JunctionBox:
    """Manages junction boxes and their electrical connections.

    Provides both incremental (one connection at a time) and bulk operations
    for connecting junction boxes and analyzing the resulting circuits.
    """

    def __init__(self, points: list[Point]):
        """Initialize with a list of junction box positions.

        Args:
            points: List of Point objects representing junction box locations
        """
        self.points = points
        self.uf = UnionFind(len(points))
        self._connections: list[tuple[int, int, int]] = []  # (dist_sq, i, j)

    def add_connection(self, i: int, j: int, dist_sq: int = None) -> bool:
        """Add a single connection between points i and j.

        Args:
            i: Index of first junction box
            j: Index of second junction box
            dist_sq: Optional squared distance (for record keeping)

        Returns:
            True if a new connection was made (points weren't already connected),
            False if points were already in the same circuit
        """
        if dist_sq is not None:
            self._connections.append((dist_sq, i, j))

        were_connected = self.uf.connected(i, j)
        self.uf.union(i, j)
        return not were_connected

    def add_connections(self, edges: list[tuple[int, tuple[int, int]]]) -> int:
        """Bulk add multiple connections.

        Args:
            edges: List of (distance_squared, (i, j)) tuples representing connections

        Returns:
            Number of new connections made (excludes redundant connections)
        """
        count = 0
        for dist_sq, (i, j) in edges:
            if self.add_connection(i, j, dist_sq):
                count += 1
        return count

    def num_circuits(self) -> int:
        """Count the number of separate circuits.

        Returns:
            Number of disconnected circuit components
        """
        roots = set(self.uf.find(i) for i in range(len(self.points)))
        return len(roots)

    def get_circuits(self) -> list[list[int]]:
        """Get all circuits as lists of point indices.

        Returns:
            List of circuits, where each circuit is a list of junction box indices
        """
        circuits: dict[int, list[int]] = defaultdict(list)
        for i in range(len(self.points)):
            root = self.uf.find(i)
            circuits[root].append(i)
        return list(circuits.values())

    def circuit_sizes(self) -> list[int]:
        """Get sorted list of circuit sizes.

        Returns:
            List of circuit sizes in ascending order
        """
        return sorted(len(c) for c in self.get_circuits())

    def get_connections(self) -> list[tuple[int, int, int]]:
        """Get the history of connections made.

        Returns:
            List of (dist_sq, i, j) tuples for all connections added
        """
        return self._connections.copy()


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

    Computes all pairwise distances and sorts them, returning the n smallest.

    Args:
        points: List of points to find nearest neighbors among
        n: Number of closest pairs to return (if None, returns all pairs)

    Returns:
        List of (distance_squared, (index_i, index_j)) tuples, sorted by distance.
        Indices satisfy i > j (each pair appears once).
    """
    n_points = len(points)
    max_pairs = n_points * (n_points - 1) // 2

    if n is None:
        n = max_pairs

    # Compute all pairwise distances
    all_distances = []
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if i <= j:
                continue
            dist_sq = p.dist_sq(q)
            all_distances.append((dist_sq, (i, j)))

    # Sort and return the n smallest
    all_distances.sort()
    return all_distances[:n]


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
        help="Number of closest pairs to connect"
    )
    args = parser.parse_args()

    points = get_inputs(args.input_file)

    # Validate n_connections
    max_pairs = len(points) * (len(points) - 1) // 2
    if args.n_connections <= 0:
        parser.error(f"n_connections must be positive, got {args.n_connections}")
    if args.n_connections >= max_pairs:
        parser.error(f"n_connections must be less than {max_pairs} (total possible pairs), got {args.n_connections}")

    # Compute all pairwise distances once (sorted by distance)
    all_edges = nearest_n_neighbours(points, n=None)

    # Part 1: Connect the first n_connections closest pairs
    print("Part 1")
    jb = JunctionBox(points)
    jb.add_connections(all_edges[:args.n_connections])
    circuit_sizes = jb.circuit_sizes()
    result = functools.reduce(operator.mul, circuit_sizes[-3:])
    print(result)

    # Part 2: Continue adding connections until all boxes are in one circuit
    print("Part 2")
    for _, (i, j) in all_edges[args.n_connections:]:
        jb.add_connection(i, j)
        if jb.num_circuits() == 1:
            # Checksum: product of x-coordinates of the final connecting points
            result = points[i].x * points[j].x
            print(result)
            break

if __name__ == "__main__":
    main()
