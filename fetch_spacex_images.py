#!/usr/bin/env python3
import argparse
import requests

import url_file


def fetch_spacex_last_launch(launch_id: str) -> None:
    launch_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url=launch_url)
    response.raise_for_status()

    spacex_images = response.json()["links"]["flickr"]["original"]
    for i, image_url in enumerate(spacex_images):
        file_ext = url_file.get_extension(image_url)
        url_file.download(image_url, f"images/spacex{i}{file_ext}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch SpaceX images")
    parser.add_argument("--launch_id", help="ID of the launch", default="latest")
    args = parser.parse_args()
    fetch_spacex_last_launch(args.launch_id)
