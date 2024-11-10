## How to Use

1. **Set Directory Path**  
   Modify the `directory` variable in the script to point to the absolute path of your target folder. For example:  
   ```python
   directory = '/path/to/your/folder'
   ```

2. **Run the Script**  
   Execute the script to automatically organize your files:  
   ```bash
   python organize_files_by_date.py
   ```

### Example Directory Structure

**Before running the script:**  
```bash
/picturesByFolder/
  ├── IMG_20231110.jpg
  ├── DSC_20231109.png
  ├── notes.txt
  ├── vacation_photo.jpg
```

**After running the script:**  
```bash
/picturesByFolder/
  ├── 20231110/
  │     └── IMG_20231110.jpg
  ├── 20231109/
  │     └── DSC_20231109.png
  ├── zero/
        ├── notes.txt
        └── vacation_photo.jpg
```

## Prerequisites

- **Python 3.x**  
- Standard libraries: `os`, `shutil`, `re`

## Notes

- Ensure you have write permissions for the specified directory.  
- This script is ideal for organizing large collections of files, such as media or logs, by embedding date-based structure for easier management.
