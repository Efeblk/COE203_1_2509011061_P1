import pytest
import json
import sys
import os

# Add src to path to allow importing folder_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture(autouse=True)
def temporary_config(monkeypatch, tmp_path):
    """
    Creates a temporary config.json and monkeypatches load_categories to use it.
    """
    config_content = {
        "categories": {
            "Images": [".jpg", ".jpeg"],
            "Documents": [".pdf", ".docx"],
            "Archives": [".zip", ".rar"]
        }
    }
    config_file = tmp_path / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config_content, f)

    import folder_utils
    
    def mock_load_categories():
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config["categories"]

    monkeypatch.setattr(folder_utils, 'load_categories', mock_load_categories)
    monkeypatch.setattr(folder_utils, 'CATEGORIES', mock_load_categories())
