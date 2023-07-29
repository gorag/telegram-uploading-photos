import os
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def download(file_url: str, file_path: Path, get_params: dict = None) -> None:
    parent_path = file_path.parent
    parent_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, params=get_params)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)


def get_extension(file_url: str) -> str:
    file_path = urlsplit(file_url).path
    path, file_name = os.path.split(file_path)
    name, extension = os.path.splitext(unquote(file_name))
    return extension


def get_all_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        sys.exit("Invalid directory")
    return [
        Path.joinpath(Path(address), Path(file))
        for address, dirs, files in os.walk(directory)
        for file in files
    ]
