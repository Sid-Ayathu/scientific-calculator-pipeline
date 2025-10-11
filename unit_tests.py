import unittest
from scientific_calculator import square_root, factorial, natural_log, power

class TestCalculator(unittest.TestCase):
    """Test cases for the scientific calculator functions."""

    def test_square_root(self):
        """Test the square root function."""
        self.assertAlmostEqual(square_root(9), 3.0)
        self.assertAlmostEqual(square_root(9), 3.0)
        self.assertAlmostEqual(square_root(0), 0.0)
        # Test for ValueError on negative input
        with self.assertRaises(ValueError):
            square_root(-4)

    def test_factorial(self):
        """Test the factorial function."""
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        # Test for ValueError on negative input
        with self.assertRaises(ValueError):
            factorial(-3)
        # Test for ValueError on non-integer input
        with self.assertRaises(ValueError):
            factorial(1.5)

    def test_natural_log(self):
        """Test the natural logarithm function."""
        self.assertAlmostEqual(natural_log(1), 0.0)
        self.assertAlmostEqual(natural_log(2.71828), 1.0, places=5)
        # Test for ValueError on zero or negative input
        with self.assertRaises(ValueError):
            natural_log(0)
        with self.assertRaises(ValueError):
            natural_log(-10)

    def test_power(self):
        """Test the power function."""
        self.assertAlmostEqual(power(2, 3), 8.0)
        self.assertAlmostEqual(power(5, 0), 1.0)
        self.assertAlmostEqual(power(4, 0.5), 2.0)
        self.assertAlmostEqual(power(-2, 3), -8.0)
        self.assertAlmostEqual(power(10, -1), 0.1)

if __name__ == '__main__':
    unittest.main()
