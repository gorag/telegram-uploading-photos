#!/usr/bin/env python3
import datetime
import os

import requests
from dotenv import load_dotenv

import file_actions


def fetch_nasa_epic() -> None:
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    nasa_epic_archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
    payload = {
        "api_key": os.getenv("NASA_API_KEY"),
    }
    response = requests.get(url=nasa_epic_url, params=payload)
    response.raise_for_status()

    for i, image_metadata in enumerate(response.json()[::-1]):
        if i < number_of_images:
            image_datetime = datetime.datetime.fromisoformat(image_metadata["date"])
            image_url = f"{nasa_epic_archive_url}{image_datetime.strftime('%Y/%m/%d')}" \
                        f"/png/{image_metadata['image']}.png"
            file_actions.download(image_url, f"{image_path}{i}.png", get_params=payload)
        else:
            break


if __name__ == "__main__":
    load_dotenv()

    image_path = "images/nasa_epic"
    number_of_images = 5
    fetch_nasa_epic()
