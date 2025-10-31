import sys
import os
from os_config import organize_files, get_os_configuration

def main():
    """Main function to run the file organizer."""
    config = get_os_configuration()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) == 3:
        source_dir = sys.argv[1]
        dest_dir = sys.argv[2]
    elif len(sys.argv) == 1:
        source_dir = os.path.join(project_root, "test_source")
        dest_dir = os.path.join(project_root, "test_destination")
    else:
        print("Usage: python3 src/main.py [source_directory] [destination_directory]")
        sys.exit(1)

    print(f"Organizing files from '{source_dir}' to '{dest_dir}'")
    organize_files(source_dir, dest_dir)
    print("File organization complete.")

if __name__ == "__main__":
    main()