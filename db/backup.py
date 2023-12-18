import os
import shutil
import time


def backup_database(db_path, backup_folder, max_size_mb=1024):
    # Check if the backup folder exists, if not, create it
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Check the size of the database
    db_size = os.path.getsize(db_path) / (1024 * 1024)  # Size in MB
    if db_size > max_size_mb:
        print(f"Database size ({db_size}MB) is over the limit of {max_size_mb}MB.")
        # Here you can call a function to clean up the database or raise an error

    # Print DB Size
    print(f"Database size is currently {db_size}MB.")

    # Create a backup
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(backup_folder, f"chat_log_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"Database backed up to {backup_path}")
