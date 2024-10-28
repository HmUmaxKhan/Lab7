from typing import List
import time


def create_permutations(
    source_string: str, unique: bool = False
) -> List[str]:
    """
    Generate all permutations of a given string using recursion.

    Args:
        source_string (str): The input string to generate permutations for.
        unique (bool): Whether to remove duplicate permutations.

    Returns:
        List[str]: List of all permutations.

    Raises:
        ValueError: If the input string is empty.
    """
    # Error handling for empty input
    if not source_string:
        raise ValueError("Input string cannot be empty")

    # Base case: single character string
    if len(source_string) == 1:
        return [source_string]

    result_permutations = []
    # Try each character as the first character
    for index in range(len(source_string)):
        # Get the current character
        current_char = source_string[index]
        # Get the remaining characters
        remaining_chars = source_string[:index] + source_string[index + 1:]

        # Recursively generate permutations of remaining characters
        sub_permutations = create_permutations(remaining_chars)

        # Add current character to the beginning of each sub-permutation
        for sub_perm in sub_permutations:
            result_permutations.append(current_char + sub_perm)

    # Remove duplicates if specified
    if unique:
        return list(set(result_permutations))
    return result_permutations


def create_permutations_iteratively(
    source_string: str, unique: bool = False
) -> List[str]:
    """
    Generate all permutations of a given string using an iterative approach.

    Args:
        source_string (str): The input string to generate permutations for.
        unique (bool): Whether to remove duplicate permutations.

    Returns:
        List[str]: List of all permutations.

    Raises:
        ValueError: If the input string is empty.
    """
    if not source_string:
        raise ValueError("Input string cannot be empty")

    # Initialize with the first character
    permutations_list = [source_string[0]]

    # Process each remaining character
    for index in range(1, len(source_string)):
        new_permutations = []
        current_char = source_string[index]

        # Insert current character at each possible position in existing permutations
        for perm in permutations_list:
            for position in range(len(perm) + 1):
                new_perm = perm[:position] + current_char + perm[position:]
                new_permutations.append(new_perm)

        permutations_list = new_permutations

    if unique:
        return list(set(permutations_list))
    return permutations_list


def evaluate_performance(source_string: str):
    """
    Compare performance between recursive and iterative approaches.

    Args:
        source_string (str): Input string to test with.
    """
    # Measure recursive performance
    start_time = time.time()
    recursive_output = create_permutations(source_string)
    recursive_duration = time.time() - start_time

    # Measure iterative performance
    start_time = time.time()
    iterative_output = create_permutations_iteratively(source_string)
    iterative_duration = time.time() - start_time

    print(f"\nPerformance evaluation for string '{source_string}':")
    print(f"Recursive method: {recursive_duration:.6f} seconds")
    print(f"Iterative method: {iterative_duration:.6f} seconds")
    print(f"Total permutations generated: {len(recursive_output)}")
    print(f"Outputs match: {sorted(recursive_output) == sorted(iterative_output)}")


# Test the implementation
def execute_tests():
    """Run a series of tests to verify the implementation."""
    test_cases = [("ABC", False), ("AAB", True), ("123", False), ("AA", True)]

    for test_string, remove_dups in test_cases:
        try:
            print(
                f"\nTesting string: '{test_string}' (unique={remove_dups})"
            )
            perms = create_permutations(test_string, remove_dups)
            print(f"Generated {len(perms)} permutations: {perms}")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    # Run test cases
    execute_tests()

    # Compare performance
    evaluate_performance("ABCD")

