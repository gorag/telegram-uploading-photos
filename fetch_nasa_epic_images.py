#!/usr/bin/env python3
import argparse
import datetime
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

import file_actions


def fetch_nasa_epic(api_key: str, number_of_images: int, image_path: Path) -> None:
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    nasa_epic_archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
    payload = {
        "api_key": api_key,
    }
    response = requests.get(url=nasa_epic_url, params=payload)
    response.raise_for_status()

    for i, image_metadata in enumerate(response.json()[::-1]):
        if i < number_of_images:
            image_datetime = datetime.datetime.fromisoformat(image_metadata["date"])
            image_url = f"{nasa_epic_archive_url}{image_datetime.strftime('%Y/%m/%d')}" \
                        f"/png/{image_metadata['image']}.png"
            file_actions.download(image_url, Path(f"{image_path}{i}.png"), get_params=payload)
        else:
            break


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number_of_images",
        help="Number of fetch images",
        default=5,
        type=int
    )
    parser.add_argument(
        "--image_path",
        help="Image path",
        default="images/nasa_epic",
        type=Path
    )
    args = parser.parse_args()

    fetch_nasa_epic(nasa_api_key, args.number_of_images, args.image_path)
