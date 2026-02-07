import os
import logging

from pathlib import Path

# logging string

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = 'recommendafy'

list_of_files = [
    ".github/workflows/.gitkeep",
    "requirements.txt",
    "setup.py",
    "main.py",
    "app.py",
    "data/data.csv",
    f"{project_name}/web/static/X.mp4",
    f"{project_name}/web/templates/index.html",
    f"{project_name}/web/templates/main.html",
    f"{project_name}/web/assets/images/test.jpg",
    f"{project_name}/web/assets/stylesheet/style.css",
    f"{project_name}/research/trials.ipynb",
    f"{project_name}/research/backup_codes.ipynb",
    f"{project_name}/research/backup_codes.ipynb",
    f"{project_name}/research/files/t.csv",

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")