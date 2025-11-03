import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
import os

# Add src to path to allow importing other modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from os_config import validate_paths
from folder_utils import organize_files_in_destination, format_report

class FileOrganizerApp(tk.Tk):
    def __init__(self, dry_run_cli_state=False):
        super().__init__()
        self.title("File Organizer")
        self.geometry("650x250")

        # Make the middle column expandable
        self.columnconfigure(1, weight=1)

        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.same_place_var = tk.BooleanVar()
        self.dry_run_var = tk.BooleanVar(value=dry_run_cli_state)

        self.create_widgets()

        # If dry_run_cli_state is True, disable the checkbox
        if dry_run_cli_state:
            self.dry_run_checkbox.config(state="disabled")

    def create_widgets(self):
        # Source Directory
        tk.Label(self, text="Source Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.source_path, width=50).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self, text="Browse...", command=self.browse_source).grid(row=0, column=2, padx=10, pady=10)

        # Destination Directory
        tk.Label(self, text="Destination Directory:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.dest_path, width=50).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self, text="Browse...", command=self.browse_dest).grid(row=1, column=2, padx=10, pady=10)

        # Checkboxes
        tk.Checkbutton(self, text="Organize in the same folder", variable=self.same_place_var, command=self.toggle_dest_entry).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.dry_run_checkbox = tk.Checkbutton(self, text="Dry-run (preview changes)", variable=self.dry_run_var)
        self.dry_run_checkbox.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Organize Button
        tk.Button(self, text="Organize Files", command=self.organize_files).grid(row=3, column=1, padx=10, pady=20)

        # Status Label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
            if self.same_place_var.get():
                self.dest_path.set(path)

    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)

    def toggle_dest_entry(self):
        if self.same_place_var.get():
            self.dest_path.set(self.source_path.get())
            self.children['!entry2'].config(state="disabled")
            self.children['!button2'].config(state="disabled")
        else:
            self.children['!entry2'].config(state="normal")
            self.children['!button3'].config(state="normal")

    def organize_files(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        dry_run = self.dry_run_var.get()

        if not source:
            messagebox.showerror("Error", "Please select a source directory.")
            return

        if not dest:
            messagebox.showerror("Error", "Please select a destination directory.")
            return

        source_path = Path(source)
        dest_path = Path(dest)

        try:
            validate_paths(source_path, dest_path)

            same_place = source_path.resolve() == dest_path.resolve()
            
            stats = organize_files_in_destination(source_path, dest_path, same_place=same_place, dry_run=dry_run)

            self.status_label.config(text="File organization complete!")
            report = format_report(stats)
            messagebox.showinfo("Organization Report", report)

        except (FileNotFoundError, NotADirectoryError) as e:
            self.status_label.config(text=f"Error: {e}", fg="red")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_label.config(text=f"An unexpected error occurred: {e}", fg="red")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
