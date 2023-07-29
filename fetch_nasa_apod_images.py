#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

import file_actions


def fetch_nasa_apod(api_key: str, count: int, image_path: Path) -> None:
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count": count,
        "thumbs": True,
        "api_key": api_key,
    }
    response = requests.get(url=nasa_apod_url, params=payload)
    response.raise_for_status()
    for i, image in enumerate(response.json()):
        if image["media_type"] == "image":
            image_url = image["url"]
        else:
            image_url = image["thumbnail_url"]
        image_ext = file_actions.get_extension(image_url)
        file_actions.download(image_url, Path(f"{image_path}{i}{image_ext}"))


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number_of_images",
        help="Number of fetch images",
        default=30,
        type=int
    )
    parser.add_argument(
        "--image_path",
        help="Image path",
        default="images/nasa_apod",
        type=Path
    )
    args = parser.parse_args()
    fetch_nasa_apod(nasa_api_key, args.number_of_images, args.image_path)
