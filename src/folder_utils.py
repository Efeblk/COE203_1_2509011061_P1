from categories import CATEGORIES

def create_category_folders(dest_path):
    """
    Creates all category folders inside the destination path.
    'dest_path' should be a Path object.
    """
    print("\n--- Creating Category Folders ---")
    
    # We loop through the *keys* of the CATEGORIES dictionary
    for category_name in CATEGORIES:
        # Join the destination path with the new category folder name
        # e.g., "path/to/dest" / "Images"
        new_folder_path = dest_path / category_name
        
        # Create the folder.
        # parents=True: Creates the main destination folder if it doesn't exist.
        # exist_ok=True: Will not crash if the "Images" folder already exists.
        new_folder_path.mkdir(parents=True, exist_ok=True)
        
    print(f"All category folders ensured in: {dest_path}")