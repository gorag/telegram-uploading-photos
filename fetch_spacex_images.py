#!/usr/bin/env python3
import argparse
from pathlib import Path

import requests

import file_actions


def fetch_spacex_last_launch(launch_id: str, image_path: Path) -> None:
    launch_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url=launch_url)
    response.raise_for_status()

    spacex_images = response.json()["links"]["flickr"]["original"]
    for i, image_url in enumerate(spacex_images):
        file_ext = file_actions.get_extension(image_url)
        file_actions.download(image_url, Path(f"{image_path}{i}{file_ext}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch SpaceX images")
    parser.add_argument(
        "--launch_id",
        help="ID of the launch",
        default="latest"
    )
    parser.add_argument(
        "--image_path",
        help="Image path without extension",
        default=Path("images/spacex")
    )
    args = parser.parse_args()

    fetch_spacex_last_launch(args.launch_id, Path(args.image_path))
