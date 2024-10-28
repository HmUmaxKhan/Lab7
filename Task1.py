import os
import sys
from typing import List
import argparse


def search_file(
    root_dir: str, target_name: str, is_case_sensitive: bool = True
) -> tuple[List[str], int]:
    """
    Performs a recursive search for a specific file within a given directory.

    Args:
        root_dir (str): Directory to start searching from.
        target_name (str): Name of the file to locate.
        is_case_sensitive (bool): If True, search is case-sensitive (default: True).

    Returns:
        tuple[List[str], int]: A tuple with:
            - A list of full file paths where the target file was located.
            - Total count of occurrences found.

    Raises:
        FileNotFoundError: If the provided directory path does not exist.
        PermissionError: If access to a directory is restricted.
    """
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Specified directory does not exist: {root_dir}")

    if not os.path.isdir(root_dir):
        raise NotADirectoryError(f"Path is not a directory: {root_dir}")

    def _recursive_find(current_dir: str) -> tuple[List[str], int]:
        """
        Internal function to recursively search files in directories.

        Args:
            current_dir (str): The current directory in the recursion.

        Returns:
            tuple[List[str], int]: Accumulated paths found and count in subdirectories.
        """
        located_paths = []
        file_count = 0

        try:
            # Retrieve directory entries
            items = os.listdir(current_dir)

            # Adjust the target name if case-insensitive search is enabled
            search_target = target_name.lower() if not is_case_sensitive else target_name

            # Iterate over each item in the directory
            for item in items:
                full_item_path = os.path.join(current_dir, item)

                # Check if it's a file and matches the target name
                if os.path.isfile(full_item_path):
                    item_name = item.lower() if not is_case_sensitive else item
                    if item_name == search_target:
                        located_paths.append(full_item_path)
                        file_count += 1

                # If a directory, continue recursion
                elif os.path.isdir(full_item_path):
                    try:
                        nested_paths, nested_count = _recursive_find(full_item_path)
                        located_paths.extend(nested_paths)
                        file_count += nested_count
                    except PermissionError:
                        print(
                            f"Warning: No permission to access directory: {full_item_path}"
                        )
                    except Exception as err:
                        print(f"Warning: Error accessing directory {full_item_path}: {err}")

        except PermissionError:
            print(f"Warning: Permission denied accessing directory: {current_dir}")
        except Exception as err:
            print(
                f"Warning: Error while searching in directory {current_dir}: {err}"
            )

        return located_paths, file_count

    # Initialize recursive search from root directory
    return _recursive_find(root_dir)


def run_search():
    """
    Parse command-line arguments and initiate the file search.
    """
    parser = argparse.ArgumentParser(
        description="Perform a recursive search for a specific file"
    )
    parser.add_argument("root_dir", help="Root directory for file search")
    parser.add_argument("target_name", help="Name of the file to find")
    parser.add_argument(
        "-ci",
        "--case-insensitive",
        action="store_true",
        help="Enable case-insensitive file search",
    )
    args = parser.parse_args()

    try:
        found_files, total_found = search_file(
            args.root_dir, args.target_name, is_case_sensitive=not args.case_insensitive
        )

        if found_files:
            print(
                f"\nLocated {total_found} instance(s) of '{args.target_name}' in these locations:"
            )
            for path in found_files:
                print(f"- {path}")
        else:
            print(f"\nNo instances of '{args.target_name}' found in '{args.root_dir}'")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    run_search()

