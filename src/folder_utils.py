from categories import CATEGORIES
from pathlib import Path
import os
import shutil

def organize_files_in_destination(source_dir, dest_dir, same_place=False):
    """
    Lists files in the source directory and copies/moves them to the corresponding destination folder.
    """
    print("\n--- Organizing Files ---")
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    for item in os.listdir(source_path):
        source_item = source_path / item
        if source_item.is_file():
            file_extension = source_item.suffix.lower()
            
            target_category = "Others" # Default category
            for category, extensions in CATEGORIES.items():
                if file_extension in extensions:
                    target_category = category
                    break
            
            dest_folder = dest_path / target_category
            dest_folder.mkdir(parents=True, exist_ok=True) # Ensure category folder exists
            
            dest_file = dest_folder / source_item.name

            # If the destination file already exists, skip it.
            # This is important for in-place organization.
            if dest_file.exists():
                print(f"Skipping {source_item.name} as it already exists in {dest_folder}")
                continue

            if same_place:
                print(f"Moving {source_item} to {dest_folder}")
                shutil.move(str(source_item), str(dest_folder))
            else:
                print(f"Copying {source_item} to {dest_folder}")
                shutil.copy(str(source_item), str(dest_folder))
