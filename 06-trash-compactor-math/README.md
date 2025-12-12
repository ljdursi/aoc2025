# Day 6: Trash Compactor Cephalopod Math

## The Problem

Cephalopod math worksheets are arranged vertically in columns. Each column contains numbers stacked vertically, with an operator (`+` or `*`) at the bottom. Columns are separated by spaces.

**Part 1:** Read each column normally (top to bottom), apply the operation, sum all results.

**Part 2 (Cephalopod Mode):** Numbers are written right-to-left! Each character position in a column forms a vertical number when read top-to-bottom.

## The Tricky Bit: Cephalopod Mode Parsing

In cephalopod mode, the column needs to be transposed so that each character position becomes a number.

### Example

Given a column slice:
```
64
23
314
```

In cephalopod mode, we transpose character positions:

```python
# Before transpose (3 rows of 3 characters):
['64 ', '23 ', '314']

# After zip(*column_lines) - reading each position vertically:
# Position 0: '6', '2', '3' → "623"
# Position 1: '4', '3', '1' → "431"
# Position 2: ' ', ' ', '4' → "4"

# Result:
[623, 431, 4]
```

The key insight: `zip(*column_lines)` transposes rows to columns, turning character positions into vertical numbers.

## Running

```bash
python3 day06.py ex01.txt
```

## Testing

```bash
python3 -m unittest test_day06 -v
```

31 tests covering both normal and cephalopod modes.
