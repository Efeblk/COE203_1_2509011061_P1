import pytest
import json
import sys
import os
from pathlib import Path

# Add src to path to allow importing folder_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from folder_utils import load_categories

@pytest.fixture
def mock_config_file(tmp_path):
    def _mock_config_file(content):
        config_file = tmp_path / "config.json"
        config_file.write_text(content)
        return config_file
    return _mock_config_file

def test_load_categories_missing_file():
    with pytest.raises(FileNotFoundError):
        load_categories("non_existent_file.json")

def test_load_categories_invalid_json(mock_config_file):
    config_file = mock_config_file("invalid json")
    with pytest.raises(ValueError, match="Error decoding JSON"):
        load_categories(config_file)

def test_load_categories_missing_categories_key(mock_config_file):
    config_file = mock_config_file('{"other_key": "value"}')
    with pytest.raises(ValueError, match="'categories' key is missing"):
        load_categories(config_file)

def test_load_categories_not_a_dict(mock_config_file):
    config_file = mock_config_file('{"categories": [1, 2, 3]}')
    with pytest.raises(ValueError, match="'categories' value must be a dictionary"):
        load_categories(config_file)

def test_load_categories_extensions_not_a_list(mock_config_file):
    config_file = mock_config_file('{"categories": {"Images": ".jpg"}}')
    with pytest.raises(ValueError, match="must be a list of extensions"):
        load_categories(config_file)

def test_load_categories_extension_not_a_string(mock_config_file):
    config_file = mock_config_file('{"categories": {"Images": [1, 2]}}')
    with pytest.raises(ValueError, match="must be strings"):
        load_categories(config_file)

def test_load_categories_valid(mock_config_file, categories_dict):
    config_file = mock_config_file(json.dumps({"categories": categories_dict}))
    categories = load_categories(config_file)
    assert categories == categories_dict
