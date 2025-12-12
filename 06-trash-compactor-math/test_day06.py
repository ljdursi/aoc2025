#!/usr/bin/env python3
"""
Unit tests for Advent of Code 2025 - Day 6
"""

import unittest
from io import StringIO
from day06 import (
    Operation,
    find_operator_positions,
    determine_column_boundaries,
    parse_column,
    parse_worksheet,
    get_inputs,
    calculate_grand_total,
)


# Test data constants
EXAMPLE_WORKSHEET = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

# Cephalopod mode requires trailing spaces
EXAMPLE_WORKSHEET_CEPHALOPOD = "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  "


class TestOperation(unittest.TestCase):
    """Tests for the Operation enum"""

    def test_from_str_add(self):
        """Test creating ADD operation from string"""
        op = Operation.from_str('+')
        self.assertEqual(op, Operation.ADD)

    def test_from_str_multiply(self):
        """Test creating MULTIPLY operation from string"""
        op = Operation.from_str('*')
        self.assertEqual(op, Operation.MULTIPLY)

    def test_from_str_invalid(self):
        """Test that invalid strings raise ValueError"""
        with self.assertRaises(ValueError):
            Operation.from_str('-')
        with self.assertRaises(ValueError):
            Operation.from_str('/')

    def test_valid_str(self):
        """Test valid_str method"""
        self.assertTrue(Operation.valid_str('+'))
        self.assertTrue(Operation.valid_str('*'))
        self.assertFalse(Operation.valid_str('-'))
        self.assertFalse(Operation.valid_str('/'))

    def test_values_list(self):
        """Test values_list returns all operation symbols"""
        values = Operation.values_list()
        self.assertIn('+', values)
        self.assertIn('*', values)
        self.assertEqual(len(values), 2)

    def test_operator_add(self):
        """Test operator method returns correct function for ADD"""
        op = Operation.ADD
        func = op.operator()
        self.assertEqual(func(3, 5), 8)

    def test_operator_multiply(self):
        """Test operator method returns correct function for MULTIPLY"""
        op = Operation.MULTIPLY
        func = op.operator()
        self.assertEqual(func(3, 5), 15)

    def test_apply_add(self):
        """Test apply method with addition"""
        op = Operation.ADD
        result = op.apply([1, 2, 3, 4])
        self.assertEqual(result, 10)

    def test_apply_multiply(self):
        """Test apply method with multiplication"""
        op = Operation.MULTIPLY
        result = op.apply([2, 3, 4])
        self.assertEqual(result, 24)

    def test_apply_single_value(self):
        """Test apply with single value"""
        op = Operation.ADD
        result = op.apply([42])
        self.assertEqual(result, 42)


class TestFindOperatorPositions(unittest.TestCase):
    """Tests for find_operator_positions function"""

    def test_find_single_operator(self):
        """Test finding a single operator"""
        result = find_operator_positions("*")
        self.assertEqual(result, [(0, '*')])

    def test_find_multiple_operators(self):
        """Test finding multiple operators with spacing"""
        result = find_operator_positions("*   +   *   +")
        self.assertEqual(result, [(0, '*'), (4, '+'), (8, '*'), (12, '+')])

    def test_find_no_operators(self):
        """Test line with no operators"""
        result = find_operator_positions("123 456")
        self.assertEqual(result, [])

    def test_find_mixed_operators(self):
        """Test finding different operator types"""
        result = find_operator_positions("+ * + *")
        self.assertEqual(result, [(0, '+'), (2, '*'), (4, '+'), (6, '*')])


class TestDetermineColumnBoundaries(unittest.TestCase):
    """Tests for determine_column_boundaries function"""

    def test_single_column(self):
        """Test boundaries for a single column"""
        operator_positions = [(0, '*')]
        result = determine_column_boundaries(operator_positions, 10)
        self.assertEqual(result, [(0, 10)])

    def test_two_columns(self):
        """Test boundaries for two columns"""
        operator_positions = [(0, '*'), (5, '+')]
        result = determine_column_boundaries(operator_positions, 10)
        # First column: 0-4, second column: 5-10 (gap at position 4)
        self.assertEqual(result, [(0, 4), (5, 10)])

    def test_four_columns_example(self):
        """Test boundaries matching the example"""
        # Operators at positions 0, 4, 8, 12 in "*   +   *   +"
        operator_positions = [(0, '*'), (4, '+'), (8, '*'), (12, '+')]
        result = determine_column_boundaries(operator_positions, 16)
        # Columns: 0-3, 4-7, 8-11, 12-16 (gaps between columns)
        self.assertEqual(result, [(0, 3), (4, 7), (8, 11), (12, 16)])

    def test_empty_operators(self):
        """Test with no operators"""
        result = determine_column_boundaries([], 10)
        self.assertEqual(result, [])


class TestParseColumn(unittest.TestCase):
    """Tests for parse_column function"""

    def test_parse_simple_column(self):
        """Test parsing a simple column of integers"""
        column_lines = ["123", "456", "789"]
        result = parse_column(column_lines, cephalopod=False)
        self.assertEqual(result, [123, 456, 789])

    def test_parse_column_with_spacing(self):
        """Test parsing a column with leading/trailing spaces"""
        column_lines = ["  123  ", "   456", "789   "]
        result = parse_column(column_lines, cephalopod=False)
        self.assertEqual(result, [123, 456, 789])

    def test_parse_column_with_empty_lines(self):
        """Test parsing a column with empty lines"""
        column_lines = ["123", "", "456", "   ", "789"]
        result = parse_column(column_lines, cephalopod=False)
        self.assertEqual(result, [123, 456, 789])

    def test_parse_single_value(self):
        """Test parsing a column with a single value"""
        column_lines = ["42"]
        result = parse_column(column_lines, cephalopod=False)
        self.assertEqual(result, [42])

    def test_parse_cephalopod_mode(self):
        """Test parsing in cephalopod mode (right-to-left, top-to-bottom)"""
        # Example: rightmost column from the problem
        # Transpose reads each character position as a vertical number
        column_lines = ["64 ", "23 ", "314"]
        result = parse_column(column_lines, cephalopod=True)
        # After transpose: pos 0: '623', pos 1: '431', pos 2: '4'
        self.assertEqual(result, [623, 431, 4])


class TestParseWorksheet(unittest.TestCase):
    """Tests for parse_worksheet function"""

    def test_parse_example_worksheet(self):
        """Test parsing the example from the problem"""
        result = parse_worksheet(EXAMPLE_WORKSHEET)

        self.assertEqual(len(result), 4)

        # First problem: 123 * 45 * 6
        vals, op = result[0]
        self.assertEqual(vals, [123, 45, 6])
        self.assertEqual(op, Operation.MULTIPLY)

        # Second problem: 328 + 64 + 98
        vals, op = result[1]
        self.assertEqual(vals, [328, 64, 98])
        self.assertEqual(op, Operation.ADD)

        # Third problem: 51 * 387 * 215
        vals, op = result[2]
        self.assertEqual(vals, [51, 387, 215])
        self.assertEqual(op, Operation.MULTIPLY)

        # Fourth problem: 64 + 23 + 314
        vals, op = result[3]
        self.assertEqual(vals, [64, 23, 314])
        self.assertEqual(op, Operation.ADD)

    def test_parse_simple_worksheet(self):
        """Test parsing a simple two-column worksheet"""
        text = """10 20
30 40
*  +"""
        result = parse_worksheet(text)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ([10, 30], Operation.MULTIPLY))
        self.assertEqual(result[1], ([20, 40], Operation.ADD))

    def test_parse_single_problem(self):
        """Test parsing a single column"""
        text = """10
20
30
*"""
        result = parse_worksheet(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ([10, 20, 30], Operation.MULTIPLY))

    def test_parse_no_operators_raises(self):
        """Test that worksheet without operators raises ValueError"""
        text = """10 20
30 40"""
        with self.assertRaises(ValueError):
            parse_worksheet(text)

    def test_parse_example_cephalopod_mode(self):
        """Test parsing the example in cephalopod mode"""
        result = parse_worksheet(EXAMPLE_WORKSHEET_CEPHALOPOD, cephalopod=True)

        self.assertEqual(len(result), 4)

        # Leftmost problem: 356 * 24 * 1 = 8544
        vals, op = result[0]
        self.assertEqual(op, Operation.MULTIPLY)
        self.assertEqual(op.apply(vals), 8544)

        # Second from left: 8 + 248 + 369 = 625
        vals, op = result[1]
        self.assertEqual(op, Operation.ADD)
        self.assertEqual(op.apply(vals), 625)

        # Third from left: 175 * 581 * 32 = 3253600
        vals, op = result[2]
        self.assertEqual(op, Operation.MULTIPLY)
        self.assertEqual(op.apply(vals), 3253600)

        # Rightmost problem: 4 + 431 + 623 = 1058
        vals, op = result[3]
        self.assertEqual(op, Operation.ADD)
        self.assertEqual(op.apply(vals), 1058)


class TestGetInputs(unittest.TestCase):
    """Integration tests for get_inputs function"""

    def test_get_inputs_example(self):
        """Test get_inputs with the example from the problem"""
        fileobj = StringIO(EXAMPLE_WORKSHEET)
        result = get_inputs(fileobj)

        self.assertEqual(len(result), 4)

        # First problem: 123 * 45 * 6 = 33210
        vals, op = result[0]
        self.assertEqual(vals, [123, 45, 6])
        self.assertEqual(op, Operation.MULTIPLY)
        self.assertEqual(op.apply(vals), 33210)

        # Second problem: 328 + 64 + 98 = 490
        vals, op = result[1]
        self.assertEqual(vals, [328, 64, 98])
        self.assertEqual(op, Operation.ADD)
        self.assertEqual(op.apply(vals), 490)

        # Third problem: 51 * 387 * 215 = 4243455
        vals, op = result[2]
        self.assertEqual(vals, [51, 387, 215])
        self.assertEqual(op, Operation.MULTIPLY)
        self.assertEqual(op.apply(vals), 4243455)

        # Fourth problem: 64 + 23 + 314 = 401
        vals, op = result[3]
        self.assertEqual(vals, [64, 23, 314])
        self.assertEqual(op, Operation.ADD)
        self.assertEqual(op.apply(vals), 401)

    def test_get_inputs_grand_total(self):
        """Test that the grand total matches the example (Part 1)"""
        fileobj = StringIO(EXAMPLE_WORKSHEET)
        problems = get_inputs(fileobj)
        grand_total = calculate_grand_total(problems)
        self.assertEqual(grand_total, 4277556)

    def test_get_inputs_cephalopod_grand_total(self):
        """Test that the cephalopod mode grand total matches the example (Part 2)"""
        fileobj = StringIO(EXAMPLE_WORKSHEET_CEPHALOPOD)
        problems = get_inputs(fileobj, cephalopod=True)
        grand_total = calculate_grand_total(problems)
        # 8544 + 625 + 3253600 + 1058 = 3263827
        self.assertEqual(grand_total, 3263827)


if __name__ == '__main__':
    unittest.main()
