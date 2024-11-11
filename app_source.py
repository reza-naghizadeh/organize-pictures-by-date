import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import shutil
import os
import re
from datetime import datetime
import logging


def flatten_directory_structure(directory, progress_bar, progress_var):
    # List all files from all subdirectories, skipping hidden files
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Skip system/hidden files starting with '.'
            if not file.startswith('.'):
                all_files.append(os.path.join(root, file))  # Save full file paths

    total_files = len(all_files)
    progress_bar['maximum'] = total_files
    progress_var.set(0)

    moved_files = 0
    for source_path in all_files:
        filename = os.path.basename(source_path)  # Get the base filename

        # Check if the file already exists in the main directory
        destination_path = os.path.join(directory, filename)

        # If the file exists, rename it (appending a number) to avoid overwriting
        if os.path.exists(destination_path):
            base_name, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(directory, f"{base_name}_{i}{ext}")
                i += 1

        try:
            # Move the file
            shutil.move(source_path, destination_path)
            moved_files += 1
            progress_var.set(moved_files)
            progress_bar.update()
        except PermissionError as e:
            logging.error(f"PermissionError: Unable to move file {filename}. Skipping... ({e})")
            continue  # Skip this file and continue with the next one
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")
            continue  # Skip this file and continue with the next one

    # After all files are moved, remove any empty directories
    for root, dirs, files in os.walk(directory, topdown=False):  # Traverse from bottom up
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # If the directory is empty
                try:
                    os.rmdir(dir_path)  # Remove empty directory
                    print(f"Removed empty directory: {dir_path}")
                except OSError as e:
                    logging.error(f"Error removing directory {dir_path}: {e}")


def organize_files_by_date(directory, replace_duplicates, progress_bar, progress_var):
    """
    Organizes files by date. Updates progress bar during the process.
    """
    zero_folder = os.path.join(directory, 'zero')
    if not os.path.exists(zero_folder):
        os.makedirs(zero_folder)

    # Get a list of all files in the directory first
    all_files = [f for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f)) and not f.startswith('.')]

    # Count total files to process
    total_files = len(all_files)
    progress_bar['maximum'] = total_files
    progress_var.set(0)

    # Define regex patterns for different date formats
    date_patterns = [
        (r'(\d{4})/(\d{1,2})/(\d{1,2})', "%Y/%m/%d"),
        (r'(\d{4})/([A-Za-z]+|[A-Za-z]{3})/(\d{1,2})', "%Y/%B/%d"),
        (r'(\d{4})/([A-Za-z]{3})/(\d{1,2})', "%Y/%b/%d"),
        (r'(\d{2})/([A-Za-z]{3})-(\d{2})', "%y/%b-%d"),
        (r'(\d{4})/(\d{1,2})', "%Y/%m"),
        (r'(\d{4})/W(\d{1,2})', "%Y/W%U"),
        (r'(\d{8})', "%Y%m%d"),
        (r'(\d{4}):([A-Za-z]+):(\d{1,2})', "%Y:%B:%d"),
        (r'(\d{4})-(\d{2})-(\d{2})', "%Y-%m-%d"),
        (r'(\d{6})', "%Y%m"),
        (r'(\d{4})', "%Y"),
        (r'(\d{13})', "%Y%m%d%H%M%S"),  # Handle Unix-like timestamps (13 digits)
    ]

    moved_files = 0
    for filename in all_files:
        source_path = os.path.join(directory, filename)

        if os.path.isdir(source_path):  # Skip directories
            continue

        # Skip system files and those already moved to the zero folder
        if filename.startswith('.') or os.path.exists(os.path.join(zero_folder, filename)):
            print(f"Skipping already moved or system file: {filename}")
            continue

        matched = False  # Flag to check if the date is matched in any of the patterns

        for pattern, date_format in date_patterns:
            match = re.search(pattern, filename)
            if match:
                matched = True
                date_str = match.group(0)
                try:
                    # Try to parse the date using the matched format
                    valid_date = datetime.strptime(date_str, date_format)
                    print(f"Matched date: {date_str} -> {valid_date}")
                except ValueError as e:
                    print(f"Failed to parse date: {date_str} -> Error: {e}")
                    # Move to 'zero' folder if unable to parse date
                    destination_path = os.path.join(zero_folder, filename)
                    try:
                        shutil.move(source_path, destination_path)
                        moved_files += 1
                        progress_var.set(moved_files)
                        progress_bar.update()
                    except PermissionError as e:
                        logging.error(f"PermissionError while moving {filename} to 'zero' folder: {e}")
                    except Exception as e:
                        logging.error(f"Error moving {filename} to 'zero' folder: {e}")
                    continue  # Skip further processing for this file

                # Format the date into a folder name
                date_folder = os.path.join(directory, valid_date.strftime("%Y-%m-%d"))
                if not os.path.exists(date_folder):
                    os.makedirs(date_folder)

                destination_path = os.path.join(date_folder, filename)

                if os.path.exists(destination_path):
                    if replace_duplicates == 1:
                        base_name, ext = os.path.splitext(filename)
                        i = 1
                        while os.path.exists(destination_path):
                            destination_path = os.path.join(date_folder,
                                                            f"{base_name}_{i}{ext}")
                            i += 1
                    # else: pass for the default overwrite behavior

                try:
                    shutil.move(source_path, destination_path)
                    moved_files += 1
                    progress_var.set(moved_files)
                    progress_bar.update()
                except PermissionError as e:
                    logging.error(f"PermissionError while moving {filename}: {e}")
                except Exception as e:
                    logging.error(f"Error moving {filename}: {e}")
                break  # Exit the loop once the match is found

        # If no match found, move to 'zero' folder
        if not matched:
            print(f"No match for {filename}, moving to 'zero' folder.")
            destination_path = os.path.join(zero_folder, filename)
            try:
                shutil.move(source_path, destination_path)
                moved_files += 1
                progress_var.set(moved_files)
                progress_bar.update()
            except PermissionError as e:
                logging.error(f"PermissionError while moving {filename} to 'zero' folder: {e}")
            except Exception as e:
                logging.error(f"Error moving {filename} to 'zero' folder: {e}")



def select_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)


def start_organizing(directory_entry, replace_var, flatten_var, organize_var, progress_bar, progress_var):
    directory = directory_entry.get()
    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    replace_duplicates = replace_var.get()

    # If the "Flatten" checkbox is selected, flatten the folder structure first
    if flatten_var.get():
        flatten_directory_structure(directory, progress_bar, progress_var)
        messagebox.showinfo("Success", "Folder structure flattened!")

    # If the "Organize Files" checkbox is selected, organize the files by date
    if organize_var.get():
        try:
            organize_files_by_date(directory, replace_duplicates, progress_bar, progress_var)
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# GUI
root = tk.Tk()
root.title("Picture Organizer")

# Directory selection
tk.Label(root, text="Select Directory:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_directory(directory_entry)).grid(row=0, column=2, padx=10, pady=5)

# Checkbox for flattening directory structure
flatten_var = tk.IntVar(value=0)
flatten_checkbox = tk.Checkbutton(root, text="Flatten Folder Structure", variable=flatten_var)
flatten_checkbox.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Checkbox for organizing files by date
organize_var = tk.IntVar(value=0)
organize_checkbox = tk.Checkbutton(root, text="Organize Files", variable=organize_var)
organize_checkbox.grid(row=2, column=1, padx=10, pady=5, sticky='w')

# Checkbox for replacing duplicates
replace_var = tk.IntVar(value=0)
replace_checkbox = tk.Checkbutton(root, text="Replace Duplicates", variable=replace_var)
replace_checkbox.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Progress bar
progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(root, length=400, variable=progress_var, mode="determinate")
progress_bar.grid(row=4, column=1, padx=10, pady=20)

# Start button
tk.Button(root, text="Start",
          command=lambda: start_organizing(directory_entry, replace_var, flatten_var, organize_var, progress_bar,
                                           progress_var)).grid(row=5, column=1, pady=20)

# Main loop
root.mainloop()
