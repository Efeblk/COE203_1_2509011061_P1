import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gui import FileOrganizerApp

@pytest.fixture
def app():
    """Provides a clean instance of the app for each test."""
    # We don't want a real Tk window to appear during tests
    with patch('tkinter.Tk.mainloop'), patch('tkinter.Tk.geometry'), patch('tkinter.Tk.title'):
        instance = FileOrganizerApp()
        yield instance
        instance.destroy()

# 1. Input Validation
def test_organize_files_no_source(app, monkeypatch):
    """1. Test that an error message is shown if the source directory is empty."""
    mock_showerror = MagicMock()
    monkeypatch.setattr("tkinter.messagebox.showerror", mock_showerror)
    
    app.organize_files()
    
    mock_showerror.assert_called_once_with("Error", "Please select a source directory.")

def test_organize_files_no_destination(app, monkeypatch):
    """2. Test that an error message is shown if the destination directory is empty."""
    mock_showerror = MagicMock()
    monkeypatch.setattr("tkinter.messagebox.showerror", mock_showerror)
    
    app.source_path.set("some/path")
    app.organize_files()
    
    mock_showerror.assert_called_once_with("Error", "Please select a destination directory.")

# 2. UI State and Interaction
def test_toggle_dest_entry_disabled(app):
    """3. Test that checking 'Organize in same folder' disables destination controls."""
    app.same_place_var.set(True)
    app.toggle_dest_entry()
    assert app.children['!entry2'].cget('state') == 'disabled'
    assert app.children['!button2'].cget('state') == 'disabled'

def test_toggle_dest_entry_enabled(app):
    """4. Test that unchecking 'Organize in same folder' enables destination controls."""
    # First disable it
    app.same_place_var.set(True)
    app.toggle_dest_entry()
    # Then enable it
    app.same_place_var.set(False)
    app.toggle_dest_entry()
    assert app.children['!entry2'].cget('state') == 'normal'
    assert app.children['!button2'].cget('state') == 'normal'

def test_same_folder_updates_dest_path(app):
    """5. Test that the destination path is automatically updated."""
    source = "/path/to/source"
    app.source_path.set(source)
    app.same_place_var.set(True)
    app.toggle_dest_entry()
    assert app.dest_path.get() == source

# 3. Backend Interaction
@patch('gui.organize_files_in_destination')
@patch('gui.load_categories')
@patch('gui.validate_paths')
def test_backend_called_for_copy(mock_validate, mock_load_cat, mock_organize, app, monkeypatch):
    """6. Test that a copy operation calls the backend with correct arguments."""
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)
    mock_organize.return_value = {'total_files': 0, 'total_size': 0, 'files_per_category': {}}
    source, dest = "/source", "/dest"
    app.source_path.set(source)
    app.dest_path.set(dest)
    mock_load_cat.return_value = {"Images": [".jpg"]}

    app.organize_files()

    mock_validate.assert_called_once()
    mock_organize.assert_called_once()
    args, kwargs = mock_organize.call_args
    assert kwargs['same_place'] is False
    assert kwargs['dry_run'] is False

@patch('gui.organize_files_in_destination')
@patch('gui.load_categories')
@patch('gui.validate_paths')
def test_backend_called_for_move(mock_validate, mock_load_cat, mock_organize, app, monkeypatch):
    """7. Test that a move operation calls the backend with same_place=True."""
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)
    mock_organize.return_value = {'total_files': 0, 'total_size': 0, 'files_per_category': {}}
    source = "/source"
    app.source_path.set(source)
    app.dest_path.set(source)
    app.same_place_var.set(True)
    mock_load_cat.return_value = {"Images": [".jpg"]}

    app.organize_files()

    mock_organize.assert_called_once()
    args, kwargs = mock_organize.call_args
    assert kwargs['same_place'] is True

@patch('gui.organize_files_in_destination')
@patch('gui.load_categories')
@patch('gui.validate_paths')
def test_backend_called_for_dry_run(mock_validate, mock_load_cat, mock_organize, app, monkeypatch):
    """8. Test that a dry-run calls the backend with dry_run=True."""
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)
    mock_organize.return_value = {'total_files': 0, 'total_size': 0, 'files_per_category': {}}
    source, dest = "/source", "/dest"
    app.source_path.set(source)
    app.dest_path.set(dest)
    app.dry_run_var.set(True)
    mock_load_cat.return_value = {"Images": [".jpg"]}

    app.organize_files()

    mock_organize.assert_called_once()
    args, kwargs = mock_organize.call_args
    assert kwargs['dry_run'] is True

# 4. Error Handling
@patch('gui.load_categories')
def test_gui_handles_config_error(mock_load_cat, app, monkeypatch):
    """9. Test that a config error from the backend is shown in the UI."""
    mock_showerror = MagicMock()
    monkeypatch.setattr("tkinter.messagebox.showerror", mock_showerror)
    error_message = "Invalid config file!"
    mock_load_cat.side_effect = ValueError(error_message)

    app.source_path.set("/source")
    app.dest_path.set("/dest")
    app.organize_files()

    mock_showerror.assert_called_once_with("Error", error_message)

# 5. Success Case
@patch('gui.format_report')
@patch('gui.organize_files_in_destination')
@patch('gui.load_categories')
@patch('gui.validate_paths')
def test_success_shows_report(mock_validate, mock_load_cat, mock_organize, mock_format, app, monkeypatch):
    """10. Test that a successful run shows the report."""
    mock_showinfo = MagicMock()
    monkeypatch.setattr("tkinter.messagebox.showinfo", mock_showinfo)
    report_content = "--- Report ---"
    mock_format.return_value = report_content

    app.source_path.set("/source")
    app.dest_path.set("/dest")
    app.organize_files()

    assert app.status_label.cget("text") == "File organization complete!"
    mock_showinfo.assert_called_once_with("Organization Report", report_content)
