import os
import shutil
import re


def organize_files_by_date(directory):
        # Regular expression pattern to find date in the format YYYYMMDD
        date_pattern = re.compile(r'\d{8}')

        # Path for the 'zero' folder
        zero_folder = os.path.join(directory, 'zero')

        # Create the 'zero' folder if it doesn't exist
        if not os.path.exists(zero_folder):
                os.makedirs(zero_folder)

        # Iterate over all the files in the directory
        for filename in os.listdir(directory):
                source_path = os.path.join(directory, filename)

                # Skip directories to avoid moving the 'zero' folder into itself
                if os.path.isdir(source_path):
                        continue

                # Search for the date in the filename
                match = date_pattern.search(filename)
                if match:
                        # Extract the date
                        date = match.group()

                        # Create the date folder path
                        date_folder = os.path.join(directory, date)

                        # Create the date folder if it doesn't exist
                        if not os.path.exists(date_folder):
                                os.makedirs(date_folder)

                        # Move the file to the corresponding date folder
                        destination_path = os.path.join(date_folder, filename)
                        shutil.move(source_path, destination_path)
                        print(f"Moved {filename} to {date_folder}")
                else:
                        # If no date is found, move the file to the 'zero' folder
                        destination_path = os.path.join(zero_folder, filename)
                        shutil.move(source_path, destination_path)
                        print(f"Moved {filename} to {zero_folder}")


if __name__ == "__main__":
        # Specify the directory containing the files
        directory = '/Volumes/ADATA HD700/private/picturesByFolder'

        # Organize files by date
        organize_files_by_date(directory)
