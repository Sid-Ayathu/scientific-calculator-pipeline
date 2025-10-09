import math

def square_root(x):
    """Calculates the square root of a number."""
    if x < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(x)

def factorial(x):
    """Calculates the factorial of a non-negative integer."""
    if not isinstance(x, int) or x < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    return math.factorial(x)

def natural_log(x):
    """Calculates the natural logarithm (base e) of a number."""
    if x <= 0:
        raise ValueError("Natural logarithm is only defined for positive numbers.")
    return math.log(x)

def power(x, b):
    """Calculates x raised to the power of b."""
    return math.pow(x, b)

def main():
    """Main function to run the calculator menu."""
    while True:
        print("\n--- Scientific Calculator ---")
        print("1. Square Root (√x)")
        print("2. Factorial (!x)")
        print("3. Natural Logarithm (ln(x))")
        print("4. Power function (x^b)")
        print("5. Exit")

        try:
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                num = float(input("Enter a number: "))
                print(f"Result: √{num} = {square_root(num)}")
            elif choice == '2':
                num = int(input("Enter a non-negative integer: "))
                print(f"Result: !{num} = {factorial(num)}")
            elif choice == '3':
                num = float(input("Enter a positive number: "))
                print(f"Result: ln({num}) = {natural_log(num)}")
            elif choice == '4':
                base = float(input("Enter the base (x): "))
                exponent = float(input("Enter the exponent (b): "))
                print(f"Result: {base}^{exponent} = {power(base, exponent)}")
            elif choice == '5':
                print("Exiting calculator. Bye bye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
