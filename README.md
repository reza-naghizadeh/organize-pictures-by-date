How to Use:
Set Directory Path: Modify the directory variable with the absolute path to your target folder.
Run the Script: Execute the script to automatically organize your files.
Example Directory Structure:
Before running the script:

/picturesByFolder/

  ├── IMG_20231110.jpg
  
  ├── DSC_20231109.png
  
  ├── notes.txt
  
  ├── vacation_photo.jpg


After running the script:

/picturesByFolder/
    ├── 20231110/
    │     └── IMG_20231110.jpg
    ├── 20231109/
    │     └── DSC_20231109.png
    ├── zero/
        ├── notes.txt
        └── vacation_photo.jpg
        

Prerequisites:
Python 3.x
Standard libraries (os, shutil, re)
Notes:
Ensure you have write permissions for the specified directory.
This script is particularly useful for managing large collections of media files or logs.
