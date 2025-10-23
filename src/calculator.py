"""
Simple Calculator Module

This module provides basic arithmetic operations for demonstration purposes.
It's designed to showcase CI/CD pipeline functionality with Jenkins and TeamCity.
"""


class Calculator:
    """
    A simple calculator class with basic arithmetic operations.
    
    This class is intentionally simple to make the CI/CD concepts
    easy to understand for beginners.
    """
    
    def add(self, a, b):
        """
        Add two numbers together.
        
        Args:
            a (int/float): First number
            b (int/float): Second number
            
        Returns:
            int/float: Sum of a and b
        """
        return a + b
    
    def subtract(self, a, b):
        """
        Subtract b from a.
        
        Args:
            a (int/float): Number to subtract from
            b (int/float): Number to subtract
            
        Returns:
            int/float: Difference of a and b
        """
        return a - b
    
    def multiply(self, a, b):
        """
        Multiply two numbers.
        
        Args:
            a (int/float): First number
            b (int/float): Second number
            
        Returns:
            int/float: Product of a and b
        """
        return a * b
    
    def divide(self, a, b):
        """
        Divide a by b.
        
        Args:
            a (int/float): Numerator
            b (int/float): Denominator
            
        Returns:
            float: Quotient of a and b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base, exponent):
        """
        Raise base to the power of exponent.
        
        Args:
            base (int/float): The base number
            exponent (int/float): The exponent
            
        Returns:
            int/float: base raised to exponent
        """
        return base ** exponent


def main():
    """
    Demonstration of calculator functionality.
    This function runs when the module is executed directly.
    """
    calc = Calculator()
    
    print("=== Calculator Demo ===")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print("======================")


if __name__ == "__main__":
    main()
