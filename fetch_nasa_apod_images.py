#!/usr/bin/env python3
import os

import requests
from dotenv import load_dotenv

import file_actions


def fetch_nasa_apod(count: int) -> None:
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count": count,
        "thumbs": True,
        "api_key": os.getenv("NASA_API_KEY"),
    }
    response = requests.get(url=nasa_apod_url, params=payload)
    response.raise_for_status()
    for i, image in enumerate(response.json()):
        if image["media_type"] == "image":
            image_url = image["url"]
        else:
            image_url = image["thumbnail_url"]
        image_ext = file_actions.get_extension(image_url)
        file_actions.download(image_url, f"{image_path}{i}{image_ext}")


if __name__ == "__main__":
    load_dotenv()

    number_of_images = 30
    image_path = "images/nasa_apod"
    fetch_nasa_apod(number_of_images)
