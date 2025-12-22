#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Click the Factory Buttons

This solution uses different approaches for each part:

Part 1: Breadth-First Search (BFS)
- State: Current indicator configuration
- Actions: Press buttons to toggle lights
- Goal: Reach target indicator pattern
- Complexity: O(2^n_indicators) - manageable for small n

Part 2: Integer Linear Programming (ILP)
- Minimize: Total button presses
- Subject to: Ax = b (achieve target counter values)
- Solver: scipy.optimize.milp
- Handles large target values efficiently
"""
import argparse
from typing import TextIO
from collections import deque
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


# ============================================================================
# Problem Representation
# ============================================================================

class ButtonProblem:
    """
    Represents a factory button-pressing optimization problem.

    Each problem consists of:
    - A goal state for indicator lights
    - A set of buttons, each of which toggles specific indicators
    - Joltage requirements (unused in part 1)

    The goal is to find the minimum number of button presses needed to reach
    the target indicator configuration, starting from all lights off.
    """

    def __init__(self, goal: list[bool], button_controls: list[list[int]], joltages: list[int]):
        """
        Initialize a ButtonProblem with parsed data.

        Args:
            goal: Target state for indicator lights (True = on, False = off)
            button_controls: For each button, which indicators it toggles (1 = toggles, 0 = doesn't)
            joltages: Joltage requirements (unused for part 1)
        """
        self.goal = goal
        self.button_controls = button_controls
        self.joltages = joltages
        self.n_indicators = len(goal)
        self.n_buttons = len(button_controls)

    @classmethod
    def from_string(cls, line: str) -> 'ButtonProblem':
        """
        Parse a button problem from the AOC input format.

        Format: [goal] (button1) (button2) ... {joltages}
        - [goal]: Indicator states (. = off, # = on)
        - (button): Comma-separated indicator indices toggled by this button
        - {joltages}: Comma-separated joltage values (unused)

        Example:
            "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
            - Goal: 4 indicators with pattern [off, on, on, off]
            - 6 buttons with different toggle patterns
            - Joltages: [3, 5, 4, 7]

        Args:
            line: Input line in AOC format

        Returns:
            Parsed ButtonProblem instance
        """
        items = line.strip().split(' ')

        goal_str = items[0][1:-1]
        joltages_str = items[-1][1:-1]

        goal = [c == '#' for c in goal_str]
        joltages = [int(subitem) for subitem in joltages_str.split(',')]
        n_indicators = len(goal_str)
        n_buttons = len(items) - 2
        button_controls = [[0] * n_indicators for _ in range(n_buttons)]

        for i, button_control_str in enumerate(items[1:-1]):
            controls = [int(num_str) for num_str in button_control_str[1:-1].split(',')]
            for control in controls:
                button_controls[i][control] = 1

        return cls(goal, button_controls, joltages)

    def find_minimum_presses_part1(self) -> int | None:
        """
        Find minimum button presses for Part 1 (toggle indicators to reach goal).

        Uses BFS to explore the state space of indicator configurations.

        Returns:
            Minimum number of presses, or None if no solution exists
        """
        start_state = tuple([0] * self.n_indicators)
        goal_state = tuple(int(g) for g in self.goal)

        queue = deque([(0, start_state)])  # (presses, state)
        visited = {start_state}

        while queue:
            presses, state = queue.popleft()

            if state == goal_state:
                return presses

            # Try pressing each button
            for button_control in self.button_controls:
                new_state = self._apply_button_toggle(state, button_control)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((presses + 1, new_state))

        return None  # No solution found

    def find_minimum_presses_part2(self) -> int | None:
        """
        Find minimum button presses for Part 2 (increment counters to reach joltage targets).

        Uses Integer Linear Programming (ILP) to handle large target values efficiently.

        Returns:
            Minimum number of presses, or None if no solution exists
        """
        # Objective: minimize total button presses (sum of all xᵢ)
        c = np.ones(len(self.button_controls))

        # Constraint matrix: A @ x = targets (transpose button_controls to get counters × buttons)
        A = np.array(self.button_controls).T

        # Equality constraint: A @ x = targets (lower bound = upper bound)
        targets = np.array(self.joltages, dtype=float)
        constraints = LinearConstraint(A, targets, targets)

        # Bounds and integrality: x >= 0, all integers
        bounds = Bounds(lb=0, ub=np.inf)

        result = milp(c=c, constraints=constraints, bounds=bounds,
                     integrality=np.ones(len(self.button_controls)))

        if result.success:
            return int(round(result.fun))  # Total button presses
        else:
            return None  # No solution found

    def _apply_button_toggle(self, state: tuple[int, ...], button_control: list[int]) -> tuple[int, ...]:
        """
        Apply a button press to toggle indicators (Part 1 helper).

        Args:
            state: Current state (tuple of 0s and 1s)
            button_control: Button control pattern where button_control[i]=1 means toggle indicator i

        Returns:
            New state after toggling
        """
        new_state = list(state)
        for i, should_toggle in enumerate(button_control):
            if should_toggle:
                new_state[i] ^= 1  # Toggle
        return tuple(new_state)


# ============================================================================
# Input/Output Functions
# ============================================================================

def get_inputs(fileobj: TextIO) -> list[ButtonProblem]:
    """Generate the button problems from the input

    Args:
        fileobj: Input file object

    Returns:
        List of Button Problem objects
    """
    lines = [line.rstrip('\n') for line in fileobj.readlines() if line.strip()]

    return [ButtonProblem.from_string(line) for line in lines]


# ============================================================================
# Main Entry Point
# ============================================================================

def main() -> None:
    """
    Main entry point for the Advent of Code Day 10 solution.

    Reads button problems from an input file and computes the total minimum
    number of button presses needed across all problems.
    """
    parser = argparse.ArgumentParser(
        prog='day10',
        description="Advent of Code 2025 - Day 10: Optimal Factory Button Presses"
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType('r'),
        help="Input file containing the button press problems"
    )
    args = parser.parse_args()

    button_problems = get_inputs(args.input_file)

    print("Part 1")
    min_presses_part1 = [button_problem.find_minimum_presses_part1() for button_problem in button_problems]
    print(sum(min_presses_part1))

    print("Part 2")
    min_presses_part2 = [button_problem.find_minimum_presses_part2() for button_problem in button_problems]
    print(sum(min_presses_part2))

if __name__ == "__main__":
    main()