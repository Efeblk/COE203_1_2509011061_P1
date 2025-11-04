import json
from pathlib import Path
import os
import shutil

def load_categories(config_path=None):
    if config_path is None:
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config.json"
    else:
        config_path = Path(config_path)

    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from the configuration file: {config_path}")

    if "categories" not in config:
        raise ValueError("The 'categories' key is missing from the configuration file.")

    categories = config["categories"]
    if not isinstance(categories, dict):
        raise ValueError("The 'categories' value must be a dictionary.")

    for category, extensions in categories.items():
        if not isinstance(extensions, list):
            raise ValueError(f"The value for category '{category}' must be a list of extensions.")
        if not all(isinstance(ext, str) for ext in extensions):
            raise ValueError(f"All extensions for category '{category}' must be strings.")

    return categories

def organize_files_in_destination(source_dir, dest_dir, categories, same_place=False, dry_run=False):
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
                continue

            file_extension = source_item.suffix.lower()
            
            target_category = "Others" #default
            for category, extensions in categories.items():
                if file_extension in extensions:
                    target_category = category
                    break
            
            if target_category not in stats["files_per_category"]:
                stats["files_per_category"][target_category] = 0
            stats["files_per_category"][target_category] += 1

            dest_folder = dest_path / target_category
            
            if dry_run:
                print(f"DRY-RUN: Would {'move' if same_place else 'copy'} '{source_item.name}' to '{dest_folder}'")
                continue

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
