import json
from pathlib import Path
import os
import shutil

def load_categories():
    """Loads categories from config.json"""
    # Assuming config.json is in the project root, which is one level above src
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config["categories"]

CATEGORIES = load_categories()

def organize_files_in_destination(source_dir, dest_dir, same_place=False, dry_run=False):
    """
    Lists files in the source directory and copies/moves them to the corresponding destination folder.
    Returns a dictionary with statistics.
    """
    print("\n--- Organizing Files ---")
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    stats = {
        "total_files": 0,
        "total_size": 0,
        "files_per_category": {}
    }

    if dry_run:
        print("\n--- Starting Dry Run (no files will be moved) ---")

    for item in os.listdir(source_path):
        source_item = source_path / item
        if source_item.is_file():
            stats["total_files"] += 1
            try:
                file_size = source_item.stat().st_size
                stats["total_size"] += file_size
            except FileNotFoundError:
                # File might have been moved already in same_place mode
                continue

            file_extension = source_item.suffix.lower()
            
            target_category = "Others"
            for category, extensions in CATEGORIES.items():
                if file_extension in extensions:
                    target_category = category
                    break
            
            if target_category not in stats["files_per_category"]:
                stats["files_per_category"][target_category] = 0
            stats["files_per_category"][target_category] += 1

            dest_folder = dest_path / target_category
            
            if dry_run:
                print(f"DRY-RUN: Would {'move' if same_place else 'copy'} '{source_item.name}' to '{dest_folder}'")
                continue # Skip the actual file operation

            dest_folder.mkdir(parents=True, exist_ok=True)
            
            dest_file = dest_folder / source_item.name

            if dest_file.exists():
                print(f"Skipping {source_item.name} as it already exists in {dest_folder}")
                continue

            if same_place:
                print(f"Moving {source_item} to {dest_folder}")
                shutil.move(str(source_item), str(dest_folder))
            else:
                print(f"Copying {source_item} to {dest_folder}")
                shutil.copy(str(source_item), str(dest_folder))
    
    return stats

def format_report(stats):
    """Formats the statistics into a string."""
    report = "\n--- Organization Report ---\n"
    report += f"Total files processed: {stats['total_files']}\n"
    
    total_size_kb = stats['total_size'] / 1024
    total_size_mb = total_size_kb / 1024
    total_size_gb = total_size_mb / 1024
    
    if total_size_gb >= 1:
        report += f"Total size of files: {total_size_gb:.2f} GB\n"
    elif total_size_mb >= 1:
        report += f"Total size of files: {total_size_mb:.2f} MB\n"
    elif total_size_kb >= 1:
        report += f"Total size of files: {total_size_kb:.2f} KB\n"
    else:
        report += f"Total size of files: {stats['total_size']} bytes\n"

    report += "\nFiles per category:\n"
    for category, count in stats["files_per_category"].items():
        report += f"- {category}: {count}\n"
    report += "---------------------------\n"
    return report
