# File Organizer

This Python script helps organize files in a specified directory into category-based subdirectories.

## Features

- Organizes files by their extension into predefined categories (e.g., Images, Documents, Videos).
- Creates new category directories if they don't exist.
- Handles files with unknown extensions by placing them in an 'Others' directory.

## Usage

1.  **Place the script:** The main script is located at `src/main.py`.

2.  **Modify the script (Optional):**
    - Open `src/main.py`.
    - In the `if __name__ == "__main__":` block, uncomment and set `source_directory` to the path of the folder you want to organize.
    - Set `destination_directory` to the path where you want the organized files to be moved. This can be the same as the source directory or a different one.

    ```python
    if __name__ == "__main__":
        source_directory = "/path/to/your/source/folder"
        destination_directory = "/path/to/your/destination/folder"
        organize_files(source_directory, destination_directory)
    ```

3.  **Run the script:** Execute the script from your terminal:

    ```bash
    python src/main.py
    ```

## Categories

The script currently supports the following categories:

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

## Customization

You can easily customize the categories and their associated file extensions by modifying the `categories` dictionary within the `organize_files` function in `file_organizer.py`.
