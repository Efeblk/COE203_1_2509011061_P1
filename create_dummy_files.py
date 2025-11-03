import os
from pathlib import Path

def create_dummy_files(source_dir="test_source", dest_dir="test_destination"):
    """
    Creates dummy source files and a destination directory for testing the file organizer.
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    # Create directories
    source_path.mkdir(parents=True, exist_ok=True)
    dest_path.mkdir(parents=True, exist_ok=True)

    print(f"Creating dummy files in: {source_path}")

    # Define files to create with some content
    dummy_files = {
        "document1.pdf": "This is a PDF document.",
        "report.docx": "This is a Word document.",
        "image1.jpg": "Image content.",
        "photo.jpeg": "Another image.",
        "video.mp4": "Video content.",
        "song.mp3": "Audio content.",
        "archive.zip": "Archive content.",
        "spreadsheet.xlsx": "Spreadsheet data.",
        "presentation.pptx": "Presentation slides.",
        "script.py": "print('Hello, world!')",
        "webpage.html": "<html><body>Hello</body></html>",
        "unknown.xyz": "Some unknown file type.",
        "another_unknown": "File with no extension."
    }

    for filename, content in dummy_files.items():
        file_path = source_path / filename
        file_path.write_text(content)
        print(f"  Created: {file_path}")

    print(f"\nCreated empty destination directory: {dest_path}")
    print("\nDummy files and directories created successfully!")
    print(f"You can now run the file organizer: python3 src/main.py {source_dir} {dest_dir}")
    print(f"Or run the GUI: python3 src/main.py -ui")

if __name__ == "__main__":
    create_dummy_files()
