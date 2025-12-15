# Advent of Code 2025 - Day 9: Movie Theatre Tiles

## Problem Description

A movie theater has a tiled floor with red tiles at specific positions. The elves want to find the largest axis-aligned rectangle using red tiles as opposite corners.

### Part 1

Find the largest rectangle that can be formed using any two red tiles as opposite corners. No restrictions on what tiles are inside the rectangle.

### Part 2

The theater can only switch out tiles that are red or green:

- **Red tiles**: Listed in the input, one per line as x,y coordinates
- **Green tiles**: Form a polygon connecting consecutive red tiles in the input order, including:
  - Edges connecting consecutive red tiles (wrapping from last to first)
  - All tiles inside the polygon

Find the largest rectangle where:

- Opposite corners are red tiles (from the input list)
- All tiles in the rectangle (including interior) are red or green

## Solution Approach

Part 1 is straightforward: try all pairs of red tiles and calculate the area of the rectangle they form. Return the maximum.

**Time complexity**: O(n²) where n is the number of red tiles.

Part 2 is more complex due to the polygon constraint:

1. **Build the polygon**: Connect consecutive red tiles to form a potentially concave polygon

2. **For each pair of red tiles** (potential opposite corners):
   - Calculate the rectangle area
   - Check if any polygon edges cross through the rectangle
   - If valid, update the maximum area

3. **Rectangle-polygon intersection**: Check if any polygon edge crosses through the rectangle's four edges. Since both rectangles and polygon edges are grid-aligned (horizontal or vertical), this is a simple geometric check. This single test ensures the entire rectangle (including all corners and interior) stays within the polygon boundary.

**Optimizations**:

- Early termination if a rectangle can't beat the current maximum
- Bounding box checks before edge intersection tests
- Grid-aligned edge optimizations (all edges are horizontal or vertical)

**Time complexity**: O(n² × m) where n is the number of red tiles and m is the number of polygon edges.

## Usage

```bash
python3 day09.py input.txt
```

Input format: One red tile per line as comma-separated coordinates:

```csv
7,1
11,1
11,7
...
```

## Testing

Run the comprehensive test suite:

```bash
python3 -m unittest test_day09
```

The test suite includes:

- 34 unit tests covering all geometric operations
- Tests for edge cases and grid-aligned edge handling
- Validation against the problem examples
