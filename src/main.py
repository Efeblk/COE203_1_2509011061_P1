import sys
from pathlib import Path
from os_config import validate_paths
from folder_utils import create_category_folders, organize_files_in_destination

def main():
    print(f"The name of the script is: {sys.argv[0]}")
    
    arguments = sys.argv[1:]
    
    if len(arguments) == 2:
        source_directory_str = arguments[0]
        destination_directory_str = arguments[1]
    elif len(arguments) == 1 and arguments[0] == ".":
        print("Organizing files in the current directory.")
        source_directory_str = "."
        destination_directory_str = "."
    else:
        print("\nError: Please provide a valid set of arguments.")
        print(f"Usage: python {sys.argv[0]} <source_path> <destination_path>")
        print(f"   or: python {sys.argv[0]} .")
        sys.exit(1)

    # Convert to Path objects
    source_path = Path(source_directory_str)
    destination_path = Path(destination_directory_str)

    # This is the "try...except" block
    try:
        # 1. We "try" to run the function that might fail
        validate_paths(source_path, destination_path)
        create_category_folders(destination_path)

        if source_path.resolve() == destination_path.resolve():
            print("\nSource and destination are the same. Organizing files in-place (moving).")
            organize_files_in_destination(source_path, destination_path, same_place=True)
        else:
            print("\nSource and destination are different. Organizing files by copying.")
            organize_files_in_destination(source_path, destination_path)
        
        print("\n--- Success! All paths are valid. ---")
        
    except (FileNotFoundError, NotADirectoryError) as e:
        # 2. If it "catches" one of the errors we raised,
        #    it will print the error message and stop.
        print(f"\n{e}")
        sys.exit(1) # Exit the script with an error code

if __name__ == "__main__":
    main()