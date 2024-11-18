# Organize Pictures by Date

This repository contains a Python script and standalone apps for macOS and Windows to help you organize your pictures by date, with additional options for folder management.

## How to Use

### macOS and Windows Apps

1. **Download the App**  
   - [Download for macOS](https://github.com/user-attachments/files/17798006/PicOrganizer.zip)
   - [Download for Windows](https://github.com/user-attachments/files/17798626/PicOrganizerWin.zip)

2. **Run the App**  
   - Follow the prompts to select your desired option:
     - **Flatten Folders Structure**: Extracts all pictures from subfolders into the main folder and deletes the original folders.
     - **Organize Files**: Creates new folders based on the picture's date and moves the files into the appropriate folders.
     - **Rename Duplicates**: If disabled, duplicate pictures will be replaced. If enabled, duplicates will be renamed to avoid overwriting.
   
---

### Python Script

1. **Set Directory Path**  
   Modify the `directory` variable in the script to point to the absolute path of your target folder. For example:  
   ```python
   directory = '/path/to/your/folder'
   ```

2. **Run the Script**  
   Execute the script to organize your files:  
   ```bash
   python organize_files_by_date.py
   ```

---

### Example Directory Structure

#### Flatten Folders Structure  
**Before:**  
```bash
/picturesByFolder/
  ├── Folder1/
  │     └── IMG_20231110.jpg
  ├── Folder2/
        └── DSC_20231109.png
```  
**After:**  
```bash
/picturesByFolder/
  ├── IMG_20231110.jpg
  ├── DSC_20231109.png
```

#### Organize Files  
**Before:**  
```bash
/picturesByFolder/
  ├── IMG_20231110.jpg
  ├── DSC_20231109.png
  ├── notes.txt
```  
**After:**  
```bash
/picturesByFolder/
  ├── 20231110/
  │     └── IMG_20231110.jpg
  ├── 20231109/
  │     └── DSC_20231109.png
  ├── zero/
        └── notes.txt
```

#### Replace Duplicates  
If this option is enabled, duplicate files will be replaced. If disabled, duplicates will be renamed (e.g., `IMG_20231110(1).jpg`).

---

## Prerequisites for Python Script

- **Python 3.x**  
- Standard libraries: `os`, `shutil`, `re`

## Notes

- Ensure you have write permissions for the specified directory.  
- This solution is ideal for organizing large collections of files, such as media or logs, by embedding a date-based folder structure for easier management.
