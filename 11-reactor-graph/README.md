# Day 11: Reactor Graph Path Counting

## Problem

Given a directed graph of devices and their connections:

**Part 1:** Count all paths from `you` to `out`

**Part 2:** Count all paths from `svr` to `out` that visit both `fft` and `dac` (in any order)

## Solution Approach

### Part 1: BFS Path Enumeration

Uses breadth-first search to enumerate all simple paths (no cycles):
- Maintains a queue of partial paths
- Extends each path to unvisited neighbors
- Counts paths that reach the destination

**Why:** Simple and returns actual paths, suitable for smaller graphs.

### Part 2: Segmented Counting with Memoized DFS

For graphs with billions/trillions of paths, we use two optimizations:

**1. Segmented Multiplication**

Break the path into segments to avoid exponential enumeration:
- **FFT-first:** `svr → fft` × `fft → dac` × `dac → out`
- **DAC-first:** `svr → dac` × `dac → fft` × `fft → out`
- Use `avoid` lists to ensure segments don't visit milestone nodes early

**2. Memoized DFS for Counting**

Instead of enumerating paths, count them recursively:
```python
paths(A → D) = sum(paths(neighbor → D) for neighbor in A's neighbors)
```

Uses dynamic programming with memoization to cache results and avoid recomputation.

**Why:**
- Handles 300+ trillion paths in milliseconds
- Memory efficient (only stores counts, not paths)
- Memoization prevents exponential recomputation

## Performance

Example results on large input (615 nodes, 1717 edges):
```
svr → fft: 10,826 paths (0.00s)
fft → dac: 4,167,558 paths (0.00s)
dac → out: 6,716 paths (0.00s)
svr → dac: 1,075,107,709,173 paths (0.00s)
Total: 303,012,373,210,128 paths
```

## Usage

```bash
# Part 1
python3 day11.py input.txt -1

# Part 2
python3 day11.py input.txt -2

# Run tests
python3 -m unittest test_day11.py
```

## Key Insights

- **Cycle detection** is essential for simple path counting
- **Path enumeration** doesn't scale beyond thousands of paths
- **Memoization** transforms exponential problems into tractable ones
- **Segmented multiplication** works when intermediate nodes don't overlap between segments
