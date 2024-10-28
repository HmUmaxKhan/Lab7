import unittest
import os
import tempfile
import shutil
from pathlib import Path
from Task1 import search_file  # Make sure to import the search_file function


class TestFileSearcher(unittest.TestCase):
    """Unit tests for the recursive file searching functionality."""

    def setUp(self):
        """
        Creates a structured directory tree for testing the recursive file search.
        Structure created:
        sample_dir/
        ├── file1.txt
        ├── FILE1.txt
        ├── empty_folder/
        ├── folder1/
        │   ├── file2.txt
        │   └── folder2/
        │       ├── file3.txt
        │       └── folder3/
        │           └── file1.txt
        └── folder4/
            ├── file1.txt
            └── folder5/
                ├── file2.txt
                └── .hidden_folder/
                    └── file1.txt
        """
        # Create a temporary base directory for tests
        self.base_dir = tempfile.mkdtemp()

        # Define directory structure
        subdirs = [
            "empty_folder",
            "folder1/folder2/folder3",
            "folder4/folder5/.hidden_folder",
        ]

        # Create all subdirectories
        for subdir_path in subdirs:
            os.makedirs(os.path.join(self.base_dir, subdir_path))

        # Create test files with content
        self.file_data = [
            ("file1.txt", self.base_dir, "base file1"),
            ("FILE1.txt", self.base_dir, "base FILE1"),
            ("file2.txt", os.path.join(self.base_dir, "folder1"), "folder1 file2"),
            (
                "file3.txt",
                os.path.join(self.base_dir, "folder1/folder2"),
                "folder2 file3",
            ),
            (
                "file1.txt",
                os.path.join(self.base_dir, "folder1/folder2/folder3"),
                "folder3 file1",
            ),
            ("file1.txt", os.path.join(self.base_dir, "folder4"), "folder4 file1"),
            (
                "file2.txt",
                os.path.join(self.base_dir, "folder4/folder5"),
                "folder5 file2",
            ),
            (
                "file1.txt",
                os.path.join(self.base_dir, "folder4/folder5/.hidden_folder"),
                "hidden file1",
            ),
        ]

        # Create all test files
        for filename, directory, content in self.file_data:
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as f:
                f.write(content)

    def tearDown(self):
        """Remove the temporary directory after tests have run."""
        shutil.rmtree(self.base_dir)

    def test_basic_file_search(self):
        """Test basic functionality of file searching in the root directory."""
        found_paths, count = search_file(self.base_dir, "file1.txt", is_case_sensitive=True)
        self.assertEqual(count, 4)  # Should find 4 exact matches for file1.txt
        self.assertEqual(len(found_paths), 4)
        # Ensure all paths are absolute
        self.assertTrue(all(os.path.isabs(path) for path in found_paths))

    def test_nested_search(self):
        """Test searching for a file in deeply nested directories."""
        found_paths, count = search_file(self.base_dir, "file3.txt", is_case_sensitive=True)
        self.assertEqual(count, 1)
        self.assertTrue(found_paths[0].endswith(os.path.join("folder2", "file3.txt")))

    def test_search_empty_folder(self):
        """Test searching in an empty folder."""
        empty_folder = os.path.join(self.base_dir, "empty_folder")
        found_paths, count = search_file(empty_folder, "file1.txt", is_case_sensitive=True)
        self.assertEqual(count, 0)
        self.assertEqual(len(found_paths), 0)

    def test_search_hidden_folder(self):
        """Test searching within hidden folders."""
        found_paths, count = search_file(self.base_dir, "file1.txt", is_case_sensitive=True)
        hidden_path = os.path.join(self.base_dir, "folder4", "folder5", ".hidden_folder", "file1.txt")
        hidden_path = os.path.normpath(hidden_path)  # Normalize path separators
        normalized_paths = [os.path.normpath(p) for p in found_paths]
        self.assertTrue(any(path == hidden_path for path in normalized_paths))

    def test_nonexistent_path(self):
        """Test behavior when searching in a nonexistent directory."""
        with self.assertRaises(FileNotFoundError):
            search_file(os.path.join(self.base_dir, "invalid"), "file1.txt")

    def test_file_as_path(self):
        """Test behavior when a file is provided as the directory."""
        with self.assertRaises(NotADirectoryError):
            search_file(os.path.join(self.base_dir, "file1.txt"), "file2.txt")

    def test_search_empty_filename(self):
        """Test searching with an empty filename."""
        found_paths, count = search_file(self.base_dir, "", is_case_sensitive=True)
        self.assertEqual(count, 0)
        self.assertEqual(len(found_paths), 0)

    def test_special_filenames(self):
        """Test handling of filenames that contain special characters."""
        # Create a file with special characters
        special_filename = "test_!@#.txt"
        special_filepath = os.path.join(self.base_dir, special_filename)
        with open(special_filepath, "w") as f:
            f.write("special characters test")

        found_paths, count = search_file(self.base_dir, special_filename, is_case_sensitive=True)
        self.assertEqual(count, 1)
        self.assertTrue(found_paths[0].endswith(special_filename))

    def test_symlink_functionality(self):
        """Test handling of symbolic links (if supported by the OS)."""
        try:
            # Create a symlink to a directory
            symlink_path = os.path.join(self.base_dir, "symlink_to_folder1")
            os.symlink(
                os.path.join(self.base_dir, "folder1"),
                symlink_path,
                target_is_directory=True,
            )

            found_paths, count = search_file(symlink_path, "file2.txt", is_case_sensitive=True)
            self.assertEqual(count, 1)
            self.assertTrue(found_paths[0].endswith("file2.txt"))

        except (OSError, NotImplementedError):
            # Skip if the platform does not support symlinks
            self.skipTest("Symbolic links not supported on this platform")

    def test_permission_issues(self):
        """Test handling of permission denied errors."""
        restricted_dir = os.path.join(self.base_dir, "restricted_folder")
        os.makedirs(restricted_dir)

        try:
            # Try to create a file in the restricted directory
            with open(os.path.join(restricted_dir, "file1.txt"), "w") as f:
                f.write("restricted access test")

            # Remove read permissions (may not work on Windows)
            os.chmod(restricted_dir, 0o000)

            # Should not raise an exception, but print a warning
            found_paths, count = search_file(self.base_dir, "file1.txt", is_case_sensitive=True)

            # Should still find other instances of file1.txt
            self.assertTrue(count > 0)

        except PermissionError:
            self.skipTest("Unable to change permissions on this platform")
        finally:
            # Restore permissions for cleanup
            os.chmod(restricted_dir, 0o755)


if __name__ == "__main__":
    unittest.main()

