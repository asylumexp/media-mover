import os
import shutil
import keyboard
from tqdm import tqdm
import sys
import logging
import datetime

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.ERROR)  # Set the log level to ERROR or higher
console_handler.setFormatter(formatter)

# Create a file handler
current_datetime = datetime.datetime.now()
log_file_name = current_datetime.strftime("%Y-%m-%d-%H-%M-log.log")
log_file_path = rf"C:\users\wheel\Documents\logs\{log_file_name}"
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def count_files(source_folder):
    total_files = 0
    for root, dirs, files in os.walk(source_folder):
        total_files += len(files)
    return total_files


def copy_folders(source_drive, destination_drive):
    source_folder = source_drive
    destination_folder = destination_drive

    try:
        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        total_files = count_files(source_folder)

        with tqdm(total=total_files, desc="Copying files", unit="files") as pbar:
            for root, dirs, files in os.walk(source_folder):
                # Copy directories
                for dir in dirs:
                    source_path = os.path.join(root, dir)
                    relative_path = os.path.relpath(source_path, source_folder)
                    destination_path = os.path.join(
                        destination_folder, relative_path)

                    os.makedirs(destination_path, exist_ok=True)

                # Copy files
                for file in files:
                    source_file = os.path.join(root, file)
                    relative_file = os.path.relpath(source_file, source_folder)
                    destination_file = os.path.join(
                        destination_folder, relative_file)

                    try:
                        pbar.update(1)  # Increment the progress bar
                        pbar.set_postfix(
                            {"Current file": os.path.basename(source_file)})

                        if keyboard.is_pressed('esc'):
                            logger.info("File transfer stopped by user.")
                            print("File transfer stopped by user.")
                            sys.exit()

                        if os.path.exists(destination_file) and os.path.getsize(rf"{source_file}") != os.path.getsize(rf"{destination_file}"):
                            logger.info(
                                f"Replacing file: {os.path.basename(source_file)}")
                            shutil.copy2(source_file, destination_file)
                            logger.info("Successful transfer.")
                        if not os.path.exists(rf"{destination_file}"):
                            logger.info(
                                f"Current file: {os.path.basename(source_file)}")
                            shutil.copy2(source_file, destination_file)
                            logger.info("Successful transfer.")
                        else:
                            logger.info("File Exists.")

                    except Exception:
                        logger.info("Skipped transfer.")

        logger.info("All folders and files copied successfully!")
        print("All folders and files copied successfully!")

    except Exception as e:
        logger.error(f"An error occurred during the copy process: {str(e)}")
        print(f"An error occurred during the copy process: {str(e)}")

# Example usage


source_drive = r'F:\Media\TV Shows'
destination_drive = r'D:\Media\TV'
copy_folders(source_drive, destination_drive)

source_drive = r'F:\Media\Anime'
destination_drive = r'D:\Media\Anime'
copy_folders(source_drive, destination_drive)

source_drive = r'F:\Media\Movies'
destination_drive = r'D:\Media\Movies'
copy_folders(source_drive, destination_drive)
sys.stdout.close()
