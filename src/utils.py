# src/utils.py
import os
from typing import List, Dict
import logging

def setup_logging(log_file: str = "logs/app.log"):
    """Setup logging configuration"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_temp_files(temp_folder: str = "uploads/temp"):
    """Clean temporary files"""
    if os.path.exists(temp_folder):
        for file in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def get_file_list(folder: str, extension: str = None) -> List[str]:
    """Get list of files in a folder with optional extension filter"""
    if not os.path.exists(folder):
        return []
    
    files = []
    for file in os.listdir(folder):
        if extension:
            if file.endswith(extension):
                files.append(file)
        else:
            files.append(file)
    return sorted(files)