#!/usr/bin/env python3
import argparse
from typing import TextIO
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True,order=True)
class Edge():
    start: str
    end: str

class DirectedGraph:
    def __init__(self, edges: list[Edge]):
        self.nodes: list[str] = []
        self.adjacencies: dict[str, list[str]] = {}

        self.nodes = list(set([e.start for e in edges] + [e.end for e in edges]))
        for edge in edges:
            if not edge.start in self.adjacencies:
                self.adjacencies[edge.start] = [edge.end]
            else:
                self.adjacencies[edge.start].append(edge.end)

    def all_paths(self, source: str, destination: str, avoid: list[str] = None) -> list[list[str]]:
        paths: list[list[str]] = []
        avoid_set = set(avoid) if avoid else set()

        queue = deque([[source]])
        while queue:
            path_so_far = queue.popleft()
            last_node = path_so_far[-1]

            if last_node == destination:
                paths.append(path_so_far)
                continue

            if not last_node in self.adjacencies:
                continue

            path_set = set(path_so_far)  # O(1) lookups for cycle detection
            for neighbour in self.adjacencies[last_node]:
                if neighbour in path_set:  # let's not cycle
                    continue
                if neighbour in avoid_set: # don't hit nodes we're avoiding
                    continue
                queue.append(path_so_far + [neighbour])

        return paths

    def count_paths(self, source: str, destination: str, avoid: list[str] = None) -> int:
        """Count all simple paths from source to destination using memoized DFS.

        This avoids exponential path enumeration by using dynamic programming.
        Counts paths without storing them, which is critical for graphs with
        billions or trillions of paths.

        Args:
            source: Starting node
            destination: Target node
            avoid: Optional list of nodes to avoid

        Returns:
            Number of simple paths from source to destination
        """
        avoid_set = set(avoid) if avoid else set()
        memo = {}

        def count_from(node: str, visited: set) -> int:
            """Recursively count paths from node to destination.

            Uses memoization to cache results and avoid recomputation.
            Uses visited set to prevent cycles.
            """
            # Base case: reached destination
            if node == destination:
                return 1

            # Check memo cache (only valid if node not already in current path)
            if node in memo and node not in visited:
                return memo[node]

            # Dead end: no outgoing edges
            if node not in self.adjacencies:
                return 0

            # Explore all neighbors
            total = 0
            visited.add(node)

            for neighbour in self.adjacencies[node]:
                if neighbour in avoid_set:  # skip avoided nodes
                    continue
                if neighbour in visited:  # skip cycles
                    continue
                total += count_from(neighbour, visited)

            visited.remove(node)  # backtrack

            # Cache result for this node
            memo[node] = total
            return total

        return count_from(source, set())


def get_inputs(fileobj: TextIO) -> list[Edge]:
    """Parse (directed) graph edges from input file.

    Each line of input should consist of a start node name
    and a space-separated list of end node names, such as:
        aaa: you hhh
        you: bbb ccc
    Empty lines are ignored.

    Args:
        fileobj: Input file object

    Returns:
        List of Edge objects (data class of start/end node names)

    Raises:
        ValueError: If any line doesn't have exactly 2 coordinates
    """
    lines: list[str] = [line.rstrip('\n') for line in fileobj.readlines() if line.strip()]
    result: list[Edge] = []

    for line in lines:
        source, rest = line.split(':')
        destinations = rest.strip().split() 
        for dest in destinations:
            result.append(Edge(source, dest))

    return result


def main() -> None:
    """Main entry point for the solution."""
    parser = argparse.ArgumentParser(
        prog='day11',
        description="Advent of Code 2025 - Day 11: Tracing Data Flows In The Reactor"
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType('r'),
        help="Input file containing network graph"
    )
    parser.add_argument("-1", "--part_one", action='store_true')
    parser.add_argument("-2", "--part_two", action='store_true')
    args = parser.parse_args()

    edges = get_inputs(args.input_file)
    graph = DirectedGraph(edges)

    if args.part_one:
        print("Part 1")
        solutions = graph.all_paths("you", "out")
        print(len(solutions))

    if args.part_two:
        print("Part 2")
        # Break the problem into segments: count paths through both fft and dac
        # Try both orderings: fft-first and dac-first

        # FFT-first: svr -> fft -> dac -> out
        count_part_1_fft_first = graph.count_paths("svr", "fft", avoid=["dac", "out"])
        count_part_2_fft_first = graph.count_paths("fft", "dac", avoid=["svr", "out"])
        count_part_3_fft_first = graph.count_paths("dac", "out", avoid=["svr", "fft"])

        # DAC-first: svr -> dac -> fft -> out
        count_part_1_dac_first = graph.count_paths("svr", "dac", avoid=["fft", "out"])
        count_part_2_dac_first = graph.count_paths("dac", "fft", avoid=["svr", "out"])
        count_part_3_dac_first = graph.count_paths("fft", "out", avoid=["svr", "dac"])

        num_paths = count_part_1_fft_first * count_part_2_fft_first * count_part_3_fft_first
        num_paths += count_part_1_dac_first * count_part_2_dac_first * count_part_3_dac_first

        print(num_paths)


if __name__ == "__main__":
    main()