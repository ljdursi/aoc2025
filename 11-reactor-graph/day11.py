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

    def all_paths(self, source: str, destination: str) -> list[list[str]]:
        paths: list[list[str]] = []

        queue = deque([[source]])
        while queue:
            path_so_far = queue.popleft()
            last_node = path_so_far[-1]

            if last_node == destination:
                paths.append(path_so_far)
                continue

            if not last_node in self.adjacencies:
                continue

            for neighbour in self.adjacencies[last_node]:
                if neighbour in path_so_far:  # let's not cycle
                    continue
                queue.append(path_so_far + [neighbour])

        return paths


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
    args = parser.parse_args()

    edges = get_inputs(args.input_file)
    graph = DirectedGraph(edges)

    print("Part 1")
    solutions = graph.all_paths("you", "out")
    print(len(solutions))


if __name__ == "__main__":
    main()