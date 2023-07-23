from pathlib import Path
from os.path import split, splitext
from urllib.parse import urlsplit, unquote

import requests


def download(file_url: str, file_path: str, get_params: dict = None) -> None:
    parent_path = Path(file_path).parent
    Path(parent_path).mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, params=get_params)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)


def get_extension(file_url: str) -> str:
    file_path = urlsplit(file_url).path
    path, file_name = split(file_path)
    name, extension = splitext(unquote(file_name))
    return extension
