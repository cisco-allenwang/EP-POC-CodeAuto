class Calculator:
    def add(self, num1, num2):
        return num1 + num2

    def subtract(self, num1, num2):
        return num1 - num2

    def multiply(self, num1, num2):
        return num1 * num2

    def divide(self, num1, num2):
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
        
    def square(self, num):
        return num * num
    
    #add a power function to the calculation
    def power(self, base, exponent):
        return base ** exponent
    
    #add a factorial function to the calculation
    def factorial(self, num):
        if num < 0:
            return "Error: Factorial is not defined for negative numbers"
        elif num == 0:
            return 1
        else:
            result = 1
            for i in range(1, num + 1):
                result *= i
            return result
        