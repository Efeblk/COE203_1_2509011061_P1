import pytest
import json
import sys
import os

# Add src to path to allow importing folder_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def categories_dict():
    """
    Provides a sample categories dictionary for testing.
    """
    return {
        "Images": [".jpg", ".jpeg"],
        "Documents": [".pdf", ".docx"],
        "Archives": [".zip", ".rar"]
    }