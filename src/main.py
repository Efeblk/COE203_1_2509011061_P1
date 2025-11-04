import sys
from pathlib import Path
from os_config import validate_paths
from folder_utils import organize_files_in_destination, format_report, load_categories
from gui import FileOrganizerApp

def main_cli(args):
    dry_run = "--dry-run" in args
    arguments = []
    for arg in args[1:]:
        if arg not in ("--dry-run", "-ui"):
            arguments.append(arg)

    if len(arguments) == 2:
        source_path = Path(arguments[0])
        destination_path = Path(arguments[1])
    elif len(arguments) == 1 and arguments[0] == ".":
        print("Organizing files in the current directory.")
        source_path = Path(".")
        destination_path = Path(".")
    else:
        script_name = args[0]
        print(f"\nUsage: python {script_name} <source_path> <destination_path> [--dry-run]")
        print(f"   or: python {script_name} . [--dry-run]")
        print(f"   or: python {script_name} -ui [--dry-run]")
        sys.exit(1)

    try:
        categories = load_categories()
        validate_paths(source_path, destination_path)

        same_place = source_path.resolve() == destination_path.resolve()
        if same_place:
            print("\nSource and destination are the same. Organizing files in-place (moving).")
        else:
            print("\nSource and destination are different. Organizing files by copying.")

        stats = organize_files_in_destination(source_path, destination_path, categories, same_place=same_place, dry_run=dry_run)
        
        print(format_report(stats))
        print("\n--- Success! ---")
        
    except (FileNotFoundError, NotADirectoryError, ValueError) as e:
        print(f"\n{e}")
        sys.exit(1)

def main():
    use_ui = "-ui" in sys.argv
    dry_run = "--dry-run" in sys.argv

    if use_ui:
        app = FileOrganizerApp(dry_run_cli_state=dry_run)
        app.mainloop()
    else:
        main_cli(sys.argv)

if __name__ == "__main__":
    main()