# Advent of Code 2025 - Day 10: Click the Factory Buttons

## Problem Overview

Factory machines need to be configured by pressing buttons:
- **Part 1**: Toggle indicator lights to match a target pattern (binary: press 0 or 1 times)
- **Part 2**: Increment joltage counters to match target values (integer: press any number of times)

Find the minimum total button presses needed across all machines.

## Solution Approach

### Part 1: Breadth-First Search (BFS)
- **State Space**: Current indicator configuration (tuple of 0s and 1s)
- **Complexity**: O(2^n_indicators) - manageable for small n
- **Algorithm**: BFS guarantees shortest path = minimum presses
- **Why it works**: Small binary state space can be fully explored

### Part 2: Integer Linear Programming (ILP)
- **Problem**: Minimize Σxᵢ subject to Ax = b, x ≥ 0, x ∈ ℤ
  - xᵢ = number of times to press button i
  - A = button control matrix
  - b = target counter values
- **Solver**: scipy.optimize.milp
- **Why we need it**: BFS would require exploring up to Π(target values) states
  - Example: {25,23,28,53,34,54,41,12,28,22} = ~475 trillion states!
  - ILP handles this efficiently using branch-and-bound algorithms

## Setup

### Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows

# Install scipy
pip install scipy
```

## Usage

```bash
# Run with example input
./venv/bin/python3 day10.py ex01.txt

# Run with actual input
./venv/bin/python3 day10.py input01.txt

# Run tests
./venv/bin/python3 test_day10.py -v
```

## Example Results

### Example Input (ex01.txt)
```
Part 1: 7 (2 + 3 + 2)
Part 2: 33 (10 + 12 + 11)
```

### Large Values Test
```
Targets: {25,23,28,53,34,54,41,12,28,22}
Part 1: 5 presses
Part 2: 74 presses (solved in ~0.6 seconds)
```

## Code Structure

```
day10.py              # Main solution
├── Part 1: BFS Solver
│   ├── _apply_button_toggle()
│   └── _find_minimum_presses_part1()
├── Part 2: ILP Solver
│   └── _find_minimum_presses_part2_ilp()
├── ButtonProblem class
│   ├── from_string()
│   ├── find_minimum_presses_part1()
│   └── find_minimum_presses_part2()
└── main()

test_day10.py         # Unit tests
├── TestButtonProblemParsing
├── TestPart1BFS
└── TestPart2ILP
```

## Performance

| Part | Algorithm | Example Runtime | Notes |
|------|-----------|-----------------|-------|
| 1 | BFS | < 0.01s | Explores 2^n states |
| 2 (small) | ILP | < 0.01s | Targets < 20 |
| 2 (large) | ILP | ~0.6s | Targets up to 50+ |

## Key Insights

1. **Different problems need different tools**
   - Part 1: Small discrete state space → BFS
   - Part 2: Large continuous optimization → ILP

2. **State space matters**
   - Binary: 2^10 = 1,024 states (tractable)
   - Integer: 25×23×...×22 = 475 trillion states (intractable for BFS!)

3. **Mathematical structure helps**
   - Part 2 is a classic Integer Linear Program
   - Mature solvers (scipy.milp) handle this efficiently
