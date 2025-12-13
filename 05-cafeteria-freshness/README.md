# Day 5: Cafeteria Inventory Freshness

## Problem

Given ranges of "fresh" ingredient IDs and a list of ingredient IDs to check, determine:
- **Part 1**: How many ingredients are fresh (fall within any range)
- **Part 2**: The total number of unique fresh ingredient IDs possible (after accounting for overlapping ranges)

Example input:
```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

## Part 1: Counting Fresh Ingredients

**Challenge**: Check if ingredient IDs fall within any of the possibly overlapping ranges.

**Solution**: Use `contained_in_ranges()` to check each ingredient ID against all ranges using `any()`. This naturally handles overlapping ranges by returning `True` as soon as a match is found.

**Result**: For the example, `5`, `11`, and `17` are fresh → **3 fresh ingredients**.

## Part 2: Total Fresh Ingredient Capacity

**Challenge**: Ranges can overlap (e.g., `10-14` and `12-18` both cover `12-14`). Calculate the total number of unique fresh IDs without double-counting.

**Solution**: Use `merge_ranges()` to consolidate overlapping ranges:
1. Sort ranges by start value
2. Iterate through sorted ranges, merging each with the previous if they overlap
3. Sum the lengths of the merged ranges

**Why it works**: Sorting ensures we process ranges in order. The algorithm detects overlaps (including touching ranges where endpoints meet) and combines them into larger ranges. After merging `10-14`, `12-18`, and `16-20` into `10-20`, we get:
- `3-5` (length 3)
- `10-20` (length 11)

**Result**: Total capacity = **14 unique fresh ingredient IDs**.
