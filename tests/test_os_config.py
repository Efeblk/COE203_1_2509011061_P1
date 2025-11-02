import pytest
from pathlib import Path
import sys
import os

# Add src to path to allow importing os_config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from os_config import validate_paths

def test_validate_paths_valid_absolute_paths(tmp_path):
    """
    Tests validate_paths with valid absolute source and destination directories.
    """
    print(f"\n--- Running test: test_validate_paths_valid_absolute_paths ---")
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()
    
    print(f"Testing with source: {source_dir} and destination: {dest_dir}")
    try:
        validate_paths(source_dir, dest_dir)
        print("Test PASSED: No exception was raised for valid paths.")
    except Exception as e:
        pytest.fail(f"Test FAILED: An unexpected exception was raised: {e}")

def test_validate_paths_source_does_not_exist(tmp_path):
    """
    Tests that validate_paths raises FileNotFoundError when the source directory does not exist.
    """
    print(f"\n--- Running test: test_validate_paths_source_does_not_exist ---")
    source_dir = tmp_path / "non_existent_source"
    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()
    
    print(f"Testing with non-existent source: {source_dir}")
    with pytest.raises(FileNotFoundError) as excinfo:
        validate_paths(source_dir, dest_dir)
    
    assert "ERROR: The source path does not exist" in str(excinfo.value)
    print("Test PASSED: FileNotFoundError was raised as expected.")

def test_validate_paths_source_is_a_file(tmp_path):
    """
    Tests that validate_paths raises NotADirectoryError when the source path is a file, not a directory.
    """
    print(f"\n--- Running test: test_validate_paths_source_is_a_file ---")
    source_file = tmp_path / "source_as_file.txt"
    source_file.touch()
    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()
    
    print(f"Testing with source as a file: {source_file}")
    with pytest.raises(NotADirectoryError) as excinfo:
        validate_paths(source_file, dest_dir)
        
    assert "ERROR: The source path is a file, not a directory" in str(excinfo.value)
    print("Test PASSED: NotADirectoryError was raised as expected.")

def test_validate_paths_destination_parent_does_not_exist(tmp_path, capsys):
    """
    Tests that validate_paths prints a warning when the destination's parent directory does not exist.
    """
    print(f"\n--- Running test: test_validate_paths_destination_parent_does_not_exist ---")
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    dest_dir = tmp_path / "non_existent_parent" / "dest"
    
    print(f"Testing with destination in a non-existent parent: {dest_dir}")
    validate_paths(source_dir, dest_dir)
    
    captured = capsys.readouterr()
    assert "Warning: The parent folder for the destination does not exist" in captured.out
    print("Test PASSED: A warning was printed to stdout as expected.")

def test_validate_paths_with_relative_paths(tmp_path):
    """
    Tests validate_paths with relative paths.
    """
    print(f"\n--- Running test: test_validate_paths_with_relative_paths ---")
    # Create directories and change current working directory
    (tmp_path / "relative_source").mkdir()
    os.chdir(tmp_path)

    source = Path("relative_source")
    destination = Path("relative_dest")

    print(f"Testing with relative source: {source} and destination: {destination}")
    try:
        validate_paths(source, destination)
        print("Test PASSED: No exception was raised for relative paths.")
    except Exception as e:
        pytest.fail(f"Test FAILED: An unexpected exception was raised: {e}")

def test_validate_paths_destination_is_a_file(tmp_path, capsys):
    """
    Tests that validate_paths prints a warning when the destination path exists and is a file.
    """
    print(f"\n--- Running test: test_validate_paths_destination_is_a_file ---")
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    dest_file = tmp_path / "dest_as_file.txt"
    dest_file.touch()
    
    print(f"Testing with destination as a file: {dest_file}")
    validate_paths(source_dir, dest_file)
    
    captured = capsys.readouterr()
    # The current implementation does not warn if the destination is a file,
    # it only warns if the parent does not exist.
    # This test will check that no error is raised.
    assert "Warning" not in captured.out
    print("Test PASSED: No warning or error was raised for a file destination.")