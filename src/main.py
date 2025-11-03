import sys
from pathlib import Path
from os_config import validate_paths
from folder_utils import organize_files_in_destination, format_report

def main_cli(args):
    print(f"The name of the script is: {args[0]}")
    
    dry_run = "--dry-run" in args
    arguments = [arg for arg in args[1:] if arg != "--dry-run"]

    if len(arguments) == 2:
        source_directory_str = arguments[0]
        destination_directory_str = arguments[1]
    elif len(arguments) == 1 and arguments[0] == ".":
        print("Organizing files in the current directory.")
        source_directory_str = "."
        destination_directory_str = "."
    else:
        print("\nError: Please provide a valid set of arguments.")
        print(f"Usage: python {args[0]} <source_path> <destination_path> [--dry-run]")
        print(f"   or: python {args[0]} . [--dry-run]")
        print(f"   or: python {args[0]} -ui [--dry-run]")
        sys.exit(1)

    # Convert to Path objects
    source_path = Path(source_directory_str)
    destination_path = Path(destination_directory_str)

    # This is the "try...except" block
    try:
        # 1. We "try" to run the function that might fail
        validate_paths(source_path, destination_path)

        stats = None
        if source_path.resolve() == destination_path.resolve():
            print("\nSource and destination are the same. Organizing files in-place (moving).")
            stats = organize_files_in_destination(source_path, destination_path, same_place=True, dry_run=dry_run)
        else:
            print("\nSource and destination are different. Organizing files by copying.")
            stats = organize_files_in_destination(source_path, destination_path, dry_run=dry_run)
        
        print(format_report(stats))
        print("\n--- Success! All paths are valid. ---")
        
    except (FileNotFoundError, NotADirectoryError) as e:
        # 2. If it "catches" one of the errors we raised,
        #    it will print the error message and stop.
        print(f"\n{e}")
        sys.exit(1) # Exit the script with an error code

def main():
    if "-ui" in sys.argv:
        dry_run_cli = "--dry-run" in sys.argv
        from gui import FileOrganizerApp
        app = FileOrganizerApp(dry_run_cli_state=dry_run_cli)
        app.mainloop()
    else:
        main_cli(sys.argv)

if __name__ == "__main__":
    main()