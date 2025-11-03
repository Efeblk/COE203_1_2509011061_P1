# File Organizer

This Python script helps organize files in a specified directory into category-based subdirectories.

## Features

- Organizes files by their extension into predefined categories (e.g., Images, Documents, Videos).
- Handles files with unknown extensions by placing them in an 'Others' directory.
- Provides a statistical report after organization.
- Supports both Command-Line Interface (CLI) and Graphical User Interface (GUI).

## Usage

Run the program from the project's root directory.

### Command-Line Interface (CLI)

1.  **Organize files from a source to a destination directory:**
    ```bash
    python3 src/main.py <source_path> <destination_path>
    ```
    Example: `python3 src/main.py my_downloads organized_files`

2.  **Organize files in the current directory (in-place):**
    ```bash
    python3 src/main.py .
    ```

### Graphical User Interface (GUI)

To launch the GUI, use the `-ui` flag:
```bash
python3 src/main.py -ui
```

## Customization

You can easily customize the file categories and their associated extensions by modifying the `config.json` file in the project's root directory.

## Categories

The script currently supports the following categories (defined in `config.json`):

-   **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
-   **Documents:** `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`
-   **Videos:** `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`
-   **Audio:** `.mp3`, `.wav`, `.aac`, `.flac`
-   **Archives:** `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
-   **Spreadsheets:** `.xls`, `.xlsx`, `.csv`
-   **Presentations:** `.ppt`, `.pptx`
-   **Code:** `.py`, `.js`, `.html`, `.css`, `.java`, `.c`, `.cpp`, `.h`
-   **Executables:** `.exe`, `.dmg`, `.app`, `.deb`, `.rpm`
-   **Others:** Any file with an unrecognized extension.