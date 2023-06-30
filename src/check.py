import os
import subprocess

'''
# Usage
python3 src/check.py

# Description

'''

def open_folder_in_finder(folder_path):
    subprocess.run(['open', folder_path])

# Usage example
newsletter_local_dir = os.getenv('newsletter_local_dir')

open_folder_in_finder(newsletter_local_dir)
