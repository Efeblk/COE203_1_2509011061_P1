import pytest
import sys
import os
import shutil
from pathlib import Path

# Add src to path to allow importing folder_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from folder_utils import organize_files_in_destination

@pytest.fixture
def test_dirs(tmp_path):
    """
    Creates source and destination directories for testing.
    """
    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "destination"
    dest.mkdir()
    return source, dest

def test_copy_files(test_dirs, categories_dict):
    """
    Tests that files are copied correctly.
    """
    source_dir, dest_dir = test_dirs
    (source_dir / "photo.jpeg").touch()
    (source_dir / "report.docx").touch()
    (source_dir / "backup.rar").touch()
    (source_dir / "other.txt").touch()

    organize_files_in_destination(source_dir, dest_dir, categories_dict, same_place=False)

    assert (dest_dir / "Images" / "photo.jpeg").exists()
    assert (dest_dir / "Documents" / "report.docx").exists()
    assert (dest_dir / "Archives" / "backup.rar").exists()
    assert (dest_dir / "Others" / "other.txt").exists()
    # Check that original files are still in source
    assert (source_dir / "photo.jpeg").exists()

def test_move_files(test_dirs, categories_dict):
    """
    Tests that files are moved correctly.
    """
    source_dir, dest_dir = test_dirs
    (source_dir / "photo.jpeg").touch()
    (source_dir / "report.docx").touch()

    # For moving, source and dest are the same
    organize_files_in_destination(source_dir, source_dir, categories_dict, same_place=True)

    assert (source_dir / "Images" / "photo.jpeg").exists()
    assert (source_dir / "Documents" / "report.docx").exists()
    # Check that original files are gone from the root of source
    assert not (source_dir / "photo.jpeg").exists()
    assert not (source_dir / "report.docx").exists()
