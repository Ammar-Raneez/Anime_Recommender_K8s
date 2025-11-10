import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

project_name = "hotel_reservation"

list_of_files = [
    "src/__init__.py",
    "config/__init__.py",
    "utils/__init__.py",
    "pipeline/__init__.py",
    "static/style.css",
    "notebooks/research.ipynb",
    "templates/index.html",
    "setup.py",
    "requirements.txt",
]

list_of_directories = [
    "artifacts",
]


for filepath in list_of_files:
    filepath = Path(filepath)

    # ex: filedir = .github/workflows; filename = .gitkeep
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file: {filename}")

    # Create files only if they don't exist
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    for directory in list_of_directories:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Creating directory {directory}")

    else:
        logging.info(f"{filename} already exists")
