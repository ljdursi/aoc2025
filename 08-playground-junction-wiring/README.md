# Day 8: Playground Junction Wiring

## Problem

Given a list of junction boxes in 3D space:
- **Part 1**: Connect the n closest pairs and find the product of the sizes of the three largest circuits
- **Part 2**: Continue adding connections until all junction boxes are in a single circuit

## Solution

The solution uses:

1. **Nearest Neighbor Finding**: Computes all pairwise distances and sorts them, returning the n smallest. Simple O(n² log n) approach.

2. **Union-Find Data Structure**: Efficiently tracks which junction boxes belong to the same circuit as connections are made. Uses path compression and union by rank for near-constant time operations.

3. **Greedy Connection Strategy**: Connects junction boxes in order of increasing distance, similar to Kruskal's algorithm, allowing efficient circuit formation.

## Why It Works

By processing connections in order of increasing distance and using Union-Find to track components:
- Connecting already-connected boxes is a no-op (union-find handles this efficiently)
- Finding circuit membership is fast (near-constant time with path compression)
- The overall complexity is O(n² log n) for computing and sorting distances, plus O(k α(n)) for k connections, where α is the inverse Ackermann function (effectively constant)

## Running

```bash
python3 day08.py input.txt <n_connections>
```

For example, to connect the 1000 closest pairs:
```bash
python3 day08.py input.txt 1000
```

The program outputs results for both Part 1 and Part 2.

## Testing

Run the full test suite (39 tests):
```bash
python3 -m unittest test_day08 -v
```
