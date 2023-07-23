#!/usr/bin/env python3
import os

import requests
from dotenv import load_dotenv

import url_file


def fetch_nasa_apod(count: int = 30) -> None:
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count": count,
        "api_key": os.getenv("NASA_API_KEY"),
    }
    response = requests.get(url=nasa_apod_url, params=payload)
    response.raise_for_status()
    for i, image in enumerate(response.json()):
        image_url = image["url"]
        image_ext = url_file.get_extension(image_url)
        url_file.download(image_url, f"images/nasa_apod{i}{image_ext}")


if __name__ == "__main__":
    load_dotenv()
    fetch_nasa_apod()
