# GEMINI.md

## Project Overview

This project is a Python-based file organizer. It scans a specified source directory and moves files into a destination directory, sorted into subfolders based on their file extensions. The script defines several categories (Images, Documents, Videos, etc.) and their corresponding extensions.

The project is structured into several modules:
- `src/main.py`: The main entry point of the script. It handles command-line arguments and orchestrates the file organization process.
- `src/categories.py`: Defines the categories and their associated file extensions.
- `src/os_config.py`: Contains functions for validating source and destination paths.
- `src/folder_utils.py`: Provides utility functions for creating the category folders.

## Building and Running

This is a Python script and does not require a build process.

### Running the script

To run the file organizer, execute the `main.py` script from the project root directory:

```bash
python3 src/main.py [source_directory] [destination_directory]
```

- `[source_directory]`: The absolute path to the directory containing the files you want to organize.
- `[destination_directory]`: The absolute path to the directory where the organized files will be moved.

If you run the script without providing any arguments, it will use default test directories: `test_source` and `test_destination` located in the project root.

```bash
python3 src/main.py
```

## Development Conventions

- **Modularity:** The code is organized into separate files for different functionalities (e.g., `categories.py`, `folder_utils.py`).
- **Path Handling:** The script uses Python's `pathlib` library for handling file system paths in an object-oriented way.
- **Error Handling:** The script includes basic error handling, such as checking for the existence of the source directory.
- **Command-line Arguments:** The script uses `sys.argv` to accept source and destination directories as command-line arguments.
