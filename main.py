"""Run a simple calculator example."""

from calculator import add, subtract, multiply


def main() -> None:
    """Display sample calculator results."""
    first_number = 10
    second_number = 5

    print(f"{first_number} + {second_number} = {add(first_number, second_number)}")
    print(f"{first_number} - {second_number} = {subtract(first_number, second_number)}")
    print(f"{first_number} * {second_number} = {multiply(first_number, second_number)}")

if __name__ == "__main__":
    main()
