from pathlib import Path


def validate_paths(source_raw, dest_raw):
    """
    Checks if paths are valid.
    If not, it raises an exception (an error).
    """
    
    # --- Validate Source ---
    source_path = Path(source_raw)

    print(f"Analyzing source: {source_path}")

    # 1. Check if source exists at all
    if not source_path.exists():
        # This is how you "throw an error"
        raise FileNotFoundError(f"ERROR: The source path does not exist: {source_path}")

    # 2. Check if source is a directory (and not a file)
    if not source_path.is_dir():
        raise NotADirectoryError(f"ERROR: The source path is a file, not a directory: {source_path}")

    print("Source... OK")

    # --- Validate Destination ---
    # For a destination, we usually just check if its parent folder is valid
    dest_path = Path(dest_raw)
    dest_parent = dest_path.parent # The folder *containing* the destination

    print(f"Analyzing destination: {dest_path}")
    if not dest_parent.exists():
        # We'll just warn for the destination, as the script might create it
        print(f"Warning: The parent folder for the destination does not exist: {dest_parent}")

    print("Destination... OK")