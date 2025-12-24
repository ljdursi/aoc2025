# Day 12: Christmas Tree Tetris

Advent of Code 2025 - Polyomino packing problem

## Problem

Given a set of 3×3 shapes (with varying numbers of filled cells, typically 5-7) and packing requirements (grid size + shape counts), determine which requirements can be satisfied.

## Solution Approach

The solution uses **trivial case detection** to handle 100% of the actual input instantly:

### Trivial NO
If the total cells needed exceeds the grid area, packing is impossible.

```python
needed_cells = sum(count * cells_per_shape)
if needed_cells > grid_area:
    return False
```

### Trivial YES
If there are enough non-overlapping 3×3 grid regions for all shapes, packing is guaranteed.

```python
max_regions = (width // 3) * (height // 3)
if total_shapes <= max_regions:
    return True
```

### Backtracking Solver
For cases that aren't trivially decidable, a simple backtracking solver tries all placements. **This is slow** (~7 seconds for unsolvable test cases), but that's acceptable since:
- The real input (1000 cases) requires zero backtracking
- All 1000 cases are decided by trivial checks in <100ms

## Results

**Input: 1000 requirements**
- Trivial YES: 448
- Trivial NO: 552
- Needs solving: 0

**Answer: 448**

## Running

```bash
python3 day12.py input01.txt
```

## Testing

```bash
python3 -m unittest test_day12 -v
```
