# Day 8: Playground Junction Wiring

## Problem

Given a list of junction boxes in 3D space, connect the 1000 pairs that are closest together (by Euclidean distance). As pairs are connected, they form circuits. After making these connections, find the product of the sizes of the three largest circuits.

## Solution

The solution uses:

1. **Nearest Neighbor Finding**: Maintains a sorted list of the n smallest pairwise distances using binary search insertion, avoiding the need to compute and sort all O(n²) pairs.

2. **Union-Find Data Structure**: Efficiently tracks which junction boxes belong to the same circuit as connections are made. Uses path compression and union by rank for near-constant time operations.

3. **Circuit Enumeration**: After processing all connections, groups junction boxes by their root component to count circuit sizes.

## Why It Works

This is essentially Kruskal's minimum spanning forest algorithm - by processing edges (connections) in order of increasing distance and using Union-Find to track components, we efficiently build the connected circuits. The Union-Find structure ensures that:
- Connecting already-connected boxes is a no-op
- Finding circuit membership is fast
- The overall complexity is O(n² log n) for distance computation and O(k α(n)) for k connections, where α is the inverse Ackermann function (effectively constant)

## Running

```bash
python3 day08.py input.txt 1000
```

## Testing

```bash
python3 -m unittest test_day08 -v
```
