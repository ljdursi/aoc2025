#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9: Movie Theatre Tiles

This module solves the problem of finding the largest axis-aligned rectangle
that can be formed using red tiles as opposite corners.

Part 1: Find the largest rectangle using any two red tiles as opposite corners.
Part 2: Find the largest rectangle where all tiles (including interior) are
        either red or green. Green tiles form the boundary and interior of the
        polygon defined by connecting consecutive red tiles.

The solution uses:
- Point-in-polygon testing via ray casting algorithm
- Rectangle-polygon intersection testing for concave polygons
- Grid-aligned edge optimizations for integer coordinates
"""
import argparse
from typing import TextIO
from dataclasses import dataclass

@dataclass(order=True, frozen=True)
class Point:
    """Represents a point in 2D space with integer coordinates."""
    x: int
    y: int

    def area(self, q: "Point") -> int:
        """Calculate the area made between this point and another.

        Args:
            q: The other point

        Returns:
            The bounding box area
        """
        return (abs(self.x - q.x) + 1)*(abs(self.y - q.y)+ 1)

    def __str__(self) -> str:
        """Format point as comma-separated coordinates with fixed width."""
        return f"{self.x:>5},{self.y:>5}"

@dataclass(order=True, frozen=True)
class Edge:
    """Represents a line segment between two points.

    Provides geometric operations for grid-aligned edges including
    bounding box calculation, point-on-line testing, and intersection queries.

    Attributes:
        p: First endpoint of the edge
        q: Second endpoint of the edge
    """
    p: Point
    q: Point

    def bounding_box(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Calculate the axis-aligned bounding box of this edge.

        Returns:
            Tuple of ((min_x, max_x), (min_y, max_y))
        """
        xs = self.p.x, self.q.x
        ys = self.p.y, self.q.y
        return ((min(xs), max(xs)),(min(ys),max(ys)))

    def x_at_y(self, y: float) -> float:
        """Calculate the x-coordinate where this edge intersects a horizontal line at y.

        For grid-aligned edges (horizontal or vertical), uses optimized integer arithmetic.

        Args:
            y: The y-coordinate of the horizontal line

        Returns:
            The x-coordinate of the intersection point
        """
        if self.q.y == self.p.y:
            # Horizontal edge
            return min(self.p.x, self.q.x)
        if self.q.x == self.p.x:
            # Vertical edge (grid-aligned)
            return self.p.x
        # General case (though with grid-aligned edges this shouldn't happen)
        return (y - self.p.y) * (self.q.x - self.p.x) / (self.q.y - self.p.y) + self.p.x

    def collinear(self, query: Point) -> bool:
        """Test if a point lies on the infinite line defined by this edge.

        Uses cross product to determine collinearity.

        Args:
            query: The point to test

        Returns:
            True if the point is collinear with this edge's endpoints
        """
        dxc = query.x - self.p.x
        dyc = query.y - self.p.y
        dxl = self.q.x - self.p.x
        dyl = self.q.y - self.p.y

        cross = dxc * dyl - dyc * dxl
        return cross == 0


class Polygon:
    """Represents a polygon defined by vertices connected in order.

    Supports point-in-polygon testing and rectangle-polygon intersection
    for grid-aligned (axis-parallel) edges. The polygon may be concave.

    Attributes:
        points: List of vertices defining the polygon boundary
        edges: List of edges connecting consecutive vertices (wraps around)
        min_x, max_x, min_y, max_y: Bounding box of the polygon
    """

    def __init__(self, points: list[Point]):
        """Create a polygon from a list of vertices.

        Args:
            points: List of Point objects in order (clockwise or counter-clockwise).
                   Consecutive points are connected by edges, with the last point
                   connecting back to the first.
        """
        self.points: list[Point] = points
        self.edges: list[Edge] = [Edge(p,q) for p, q in zip(points, points[1:] + [points[0]])]

        self.min_x = min(p.x for p in points)
        self.max_x = max(p.x for p in points)
        self.min_y = min(p.y for p in points)
        self.max_y = max(p.y for p in points)

    def outside(self, q: Point) -> bool:
        """Test if a point is outside the polygon using ray casting algorithm.

        Casts a ray leftward (negative x direction) from the query point and counts
        how many polygon edges it crosses. An odd number of crossings means the point
        is inside; an even number (including zero) means it's outside.

        Handles special cases:
        - Points on the polygon boundary return False (considered inside)
        - Uses half-open interval [miny, maxy) to avoid double-counting at vertices
        - Optimized for grid-aligned (horizontal/vertical) edges

        Args:
            q: The point to test

        Returns:
            True if the point is outside the polygon, False if inside or on boundary
        """
        # Fast rejection: Check if point is outside polygon's bounding box
        if q.x < self.min_x or q.x > self.max_x:
            return True

        if q.y < self.min_y or q.y > self.max_y:
            return True

        # Ray casting: Count how many edges a leftward ray from q crosses
        # Odd crossings = inside, even crossings = outside
        n_crossings = 0

        for edge in self.edges:
            (minx, maxx), (miny, maxy) = edge.bounding_box()

            # Skip edges that don't span the query point's y-coordinate
            if q.y < miny or q.y > maxy:
                continue

            # Special case: Horizontal edge at same y as query point
            if miny == maxy == q.y:
                if minx <= q.x <= maxx:
                    # Point is exactly on this horizontal edge
                    return False
                # Horizontal edges don't contribute to crossing count
                continue

            # Check if point lies on this edge (non-horizontal case)
            if edge.collinear(q):
                if miny <= q.y <= maxy and minx <= q.x <= maxx:
                    # Point is on the edge boundary
                    return False

            # Half-open interval trick: Skip edges where q.y == miny
            # This prevents double-counting at vertices where two edges meet
            # We use [miny, maxy) instead of [miny, maxy]
            if q.y == miny:
                continue

            # Now check if the leftward ray from q crosses this edge
            if q.x < minx:
                # Edge is entirely to the right, ray doesn't reach it
                continue

            if q.x > maxx:
                # Edge is entirely to the left, ray definitely crosses it
                n_crossings += 1
                continue

            # Query point's x is within edge's x range
            # Calculate exact intersection point and check if ray crosses
            if edge.x_at_y(q.y) <= q.x:
                n_crossings += 1
                continue

        # Even crossings = outside, odd crossings = inside
        return n_crossings % 2 == 0

    def rectangle_crosses_boundary(self, p1: Point, p2: Point) -> bool:
        """Check if a rectangle's edges intersect any polygon edges.

        For concave polygons, a rectangle may have all four corners inside the polygon
        but still extend outside the boundary. This method detects such cases by checking
        if any of the rectangle's four edges cross any polygon edge.

        Since both the rectangle and polygon edges are grid-aligned (horizontal or vertical),
        an intersection occurs when:
        - A horizontal polygon edge crosses a vertical rectangle edge, or
        - A vertical polygon edge crosses a horizontal rectangle edge

        Args:
            p1: First corner of the rectangle
            p2: Opposite corner of the rectangle

        Returns:
            True if any rectangle edge crosses a polygon edge, False otherwise
        """
        # Calculate rectangle bounds
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)
        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)

        # The rectangle has 4 edges:
        # - Top: from (min_x, max_y) to (max_x, max_y)
        # - Bottom: from (min_x, min_y) to (max_x, min_y)
        # - Left: from (min_x, min_y) to (min_x, max_y)
        # - Right: from (max_x, min_y) to (max_x, max_y)
        #
        # For grid-aligned edges, intersections are simple:
        # - Horizontal polygon edge can only cross vertical rectangle edges
        # - Vertical polygon edge can only cross horizontal rectangle edges

        for edge in self.edges:
            edge_p1, edge_p2 = edge.p, edge.q

            if edge_p1.y == edge_p2.y:
                # Horizontal polygon edge
                edge_y = edge_p1.y
                edge_min_x = min(edge_p1.x, edge_p2.x)
                edge_max_x = max(edge_p1.x, edge_p2.x)

                # Does it cross the left side of the rectangle?
                # The horizontal edge must:
                #   1. Extend past the left side (edge_min_x < min_x < edge_max_x)
                #   2. Be within the vertical span (min_y < edge_y < max_y)
                if edge_min_x < min_x < edge_max_x and min_y < edge_y < max_y:
                    return True

                # Does it cross the right side of the rectangle?
                if edge_min_x < max_x < edge_max_x and min_y < edge_y < max_y:
                    return True

            elif edge_p1.x == edge_p2.x:
                # Vertical polygon edge
                edge_x = edge_p1.x
                edge_min_y = min(edge_p1.y, edge_p2.y)
                edge_max_y = max(edge_p1.y, edge_p2.y)

                # Does it cross the bottom side of the rectangle?
                # The vertical edge must:
                #   1. Extend past the bottom side (edge_min_y < min_y < edge_max_y)
                #   2. Be within the horizontal span (min_x < edge_x < max_x)
                if edge_min_y < min_y < edge_max_y and min_x < edge_x < max_x:
                    return True

                # Does it cross the top side of the rectangle?
                if edge_min_y < max_y < edge_max_y and min_x < edge_x < max_x:
                    return True

        # No polygon edges cross any rectangle edges
        return False


def get_inputs(fileobj: TextIO) -> list[Point]:
    """Parse red tile positions from input file.

    Each line should contain two comma-separated integers (x,y).
    Empty lines are ignored.

    Args:
        fileobj: Input file object

    Returns:
        List of Point objects

    Raises:
        ValueError: If any line doesn't have exactly 2 coordinates
    """
    lines = [line.rstrip('\n') for line in fileobj.readlines() if line.strip()]

    line_ints = [[int(item) for item in line.split(',')] for line in lines]
    if not all(len(item) == 2 for item in line_ints):
        raise ValueError("Invalid number of coordinates in a point")

    return [Point(*item) for item in line_ints]

def solve_part1(points: list[Point]) -> int:
    """Find the largest rectangle using any two points as opposite corners.

    Args:
        points: List of red tile positions

    Returns:
        The maximum area rectangle that can be formed
    """
    max_area = 0
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if i <= j:
                continue
            area = p.area(q)
            if area > max_area:
                max_area = area
    return max_area


def solve_part2(points: list[Point]) -> int:
    """Find the largest rectangle where all tiles are red or green.

    Green tiles form a polygon connecting consecutive red tiles.
    A valid rectangle must have:
    1. Red tiles at opposite corners (from the points list)
    2. All four corners inside or on the polygon boundary
    3. No polygon edges crossing through the rectangle's interior

    Args:
        points: List of red tile positions (in order, forming polygon boundary)

    Returns:
        The maximum area rectangle that fits within the polygon
    """
    max_area = 0
    polygon = Polygon(points)

    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if i <= j:
                continue

            # Early termination: Skip if this rectangle can't beat current max
            area = p.area(q)
            if area <= max_area:
                continue

            # Quick bounding box check: If rectangle extends beyond polygon bounds, skip
            rect_min_x = min(p.x, q.x)
            rect_max_x = max(p.x, q.x)
            rect_min_y = min(p.y, q.y)
            rect_max_y = max(p.y, q.y)

            if (rect_min_x < polygon.min_x or rect_max_x > polygon.max_x or
                rect_min_y < polygon.min_y or rect_max_y > polygon.max_y):
                continue

            # Check if the other two corners are inside the polygon
            corner1 = Point(p.x, q.y)
            corner2 = Point(q.x, p.y)

            if polygon.outside(corner1):
                continue
            if polygon.outside(corner2):
                continue

            # For concave polygons, check if any polygon edges
            # cross through the rectangle's edges
            if polygon.rectangle_crosses_boundary(p, q):
                continue

            max_area = area

    return max_area


def main() -> None:
    """Main entry point for the solution."""
    parser = argparse.ArgumentParser(
        prog='day09',
        description="Advent of Code 2025 - Day 9: Tiling the movie theatre"
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType('r'),
        help="Input file containing red tile positions (x,y coordinates)"
    )
    args = parser.parse_args()

    points = get_inputs(args.input_file)

    print("Part 1")
    print(solve_part1(points))

    print("Part 2")
    print(solve_part2(points))

if __name__ == "__main__":
    main()