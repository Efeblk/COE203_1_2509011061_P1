from pathlib import Path

def get_os_configuration():
    return {"os": "default"}

def validate_paths(source_raw, dest_raw):

    source_path = Path(source_raw)

    print(f"Analyzing source: {source_path}")

    if not source_path.exists():
        raise FileNotFoundError(f"ERROR: The source path does not exist: {source_path}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"ERROR: The source path is a file, not a directory: {source_path}")

    print("Source... OK")

    dest_path = Path(dest_raw)
    dest_parent = dest_path.parent

    print(f"Analyzing destination: {dest_path}")
    if not dest_parent.exists():
        print(f"Warning: The parent folder for the destination does not exist: {dest_parent}")

    print("Destination... OK")