"""
Unit Tests for Calculator Module

This test file contains both passing and potentially failing tests
to demonstrate how Jenkins and TeamCity handle test results and failures.

CONFIGURATION:
- Set ENABLE_FAILING_TESTS=true to simulate test failures
- Set ENABLE_FAILING_TESTS=false (or unset) for all tests to pass
"""

import os
import pytest
from src.calculator import Calculator


# Read environment variable to control test behavior
# This allows us to toggle failures for demonstration purposes
ENABLE_FAILING_TESTS = os.getenv('ENABLE_FAILING_TESTS', 'false').lower() == 'true'


class TestCalculatorBasic:
    """
    Basic calculator tests that always pass.
    These demonstrate successful test execution in the CI/CD pipeline.
    """
    
    def setup_method(self):
        """Set up test fixture - runs before each test method."""
        self.calc = Calculator()
    
    def test_addition_positive_numbers(self):
        """Test adding two positive numbers."""
        result = self.calc.add(5, 3)
        assert result == 8, f"Expected 8, but got {result}"
    
    def test_addition_negative_numbers(self):
        """Test adding negative numbers."""
        result = self.calc.add(-5, -3)
        assert result == -8, f"Expected -8, but got {result}"
    
    def test_subtraction(self):
        """Test basic subtraction."""
        result = self.calc.subtract(10, 4)
        assert result == 6, f"Expected 6, but got {result}"
    
    def test_multiplication(self):
        """Test basic multiplication."""
        result = self.calc.multiply(6, 7)
        assert result == 42, f"Expected 42, but got {result}"
    
    def test_division(self):
        """Test basic division."""
        result = self.calc.divide(15, 3)
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_division_by_zero(self):
        """Test that division by zero raises an error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Test exponentiation."""
        result = self.calc.power(2, 8)
        assert result == 256, f"Expected 256, but got {result}"


class TestCalculatorEdgeCases:
    """
    Edge case tests that can be toggled to fail.
    These help demonstrate error handling in CI/CD pipelines.
    """
    
    def setup_method(self):
        """Set up test fixture - runs before each test method."""
        self.calc = Calculator()
    
    def test_addition_with_zero(self):
        """Test adding zero to a number."""
        result = self.calc.add(5, 0)
        assert result == 5, f"Expected 5, but got {result}"
    
    def test_multiplication_by_zero(self):
        """Test multiplying by zero."""
        result = self.calc.multiply(100, 0)
        assert result == 0, f"Expected 0, but got {result}"
    
    @pytest.mark.skipif(
        not ENABLE_FAILING_TESTS,
        reason="Failing test disabled - set ENABLE_FAILING_TESTS=true to enable"
    )
    def test_intentional_failure_arithmetic(self):
        """
        This test intentionally fails when ENABLE_FAILING_TESTS=true.
        It demonstrates how CI/CD tools display failing tests.
        """
        result = self.calc.add(2, 2)
        # This assertion will fail - 2 + 2 = 4, not 5
        assert result == 5, "This test is designed to fail! Expected 5 but 2+2=4"
    
    @pytest.mark.skipif(
        not ENABLE_FAILING_TESTS,
        reason="Failing test disabled - set ENABLE_FAILING_TESTS=true to enable"
    )
    def test_intentional_failure_division(self):
        """
        Another intentional failure to show multiple test failures.
        """
        result = self.calc.divide(10, 2)
        # This assertion will fail - 10 / 2 = 5, not 3
        assert result == 3, "This test is designed to fail! Expected 3 but 10/2=5"


class TestCalculatorFloatingPoint:
    """
    Tests for floating-point arithmetic.
    These always pass and show successful test execution.
    """
    
    def setup_method(self):
        """Set up test fixture - runs before each test method."""
        self.calc = Calculator()
    
    def test_division_floating_point(self):
        """Test division resulting in a float."""
        result = self.calc.divide(10, 4)
        assert result == 2.5, f"Expected 2.5, but got {result}"
    
    def test_power_fractional(self):
        """Test fractional exponents (square root)."""
        result = self.calc.power(9, 0.5)
        assert abs(result - 3.0) < 0.0001, f"Expected ~3.0, but got {result}"
    
    def test_negative_power(self):
        """Test negative exponents."""
        result = self.calc.power(2, -2)
        assert result == 0.25, f"Expected 0.25, but got {result}"


# This allows running tests directly with: python -m pytest tests/test_calculator.py
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
