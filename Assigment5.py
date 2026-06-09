# Assignment5.py

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    if not isinstance(fahrenheit, (int, float)):
        raise TypeError("Temperature must be a number")
    return (fahrenheit - 32) * 5.0 / 9.0


def fibonacci(n):
    """Return the nth Fibonacci number."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# test_Assignment5.py

import unittest

class TestAssignment5(unittest.TestCase):
    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(0), -17.77777777777778)

    def test_fahrenheit_to_celsius_type_error(self):
        with self.assertRaises(TypeError):
            fahrenheit_to_celsius("thirty-two")

    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_type_error(self):
        with self.assertRaises(TypeError):
            fibonacci(3.5)

    def test_fibonacci_value_error(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)


if __name__ == "__main__":
    unittest.main()
