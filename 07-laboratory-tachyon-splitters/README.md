# Day 7: Tachyon Beam Splitters

## Problem

Tachyon beams propagate downward through a 2D grid until they hit splitters (`^`). When a beam hits a splitter, it stops and creates two new beams that continue from the row below, one column to the left and one to the right. If a beam hits a splitter that's already been hit, it's absorbed.

**Part 1**: Count how many splitters are hit by beams starting from source `S`.

**Part 2**: Count the total number of distinct paths (timelines) from the source to exiting the map.

## The Challenge

Part 2 requires counting paths through a directed acyclic graph where **paths can converge** at the same point before diverging again. For example:

```
   S
   |
   ^     (splits into 2 paths)
  / \
 ^   ^  (now 4 paths)
  \ /
   ^     (paths converge: still 4 paths through here)
  / \
 .   .   (4 distinct exit paths)
```

A naive breadth-first search fails because it may process a node before all incoming paths have been counted, leading to undercounting.

## Solution

Since beams always move downward (row numbers strictly increase along edges), we exploit this natural topological ordering:

1. Build an adjacency list from the path segments
2. Sort all nodes by `(row, col)`
3. Process nodes in sorted order, propagating path counts to successors

This guarantees that when we process a node, **all its predecessors have already been processed**, ensuring correct path counts even when multiple paths converge.

## Why It Works

The key insight: **row number provides a natural topological ordering**. Since all edges go from lower to higher row numbers, sorting by row gives us the same correctness guarantee as Kahn's algorithm, but simpler and more efficient. This is a classic example of exploiting problem structure to avoid generic graph algorithms.

## Running

```bash
python3 day07.py input.txt
python3 -m unittest test_day07.py
```
