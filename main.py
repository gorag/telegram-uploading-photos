from os.path import split, splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote
import datetime
import requests


def download_file(file_url: str, file_path: str, get_params: dict = None) -> None:
    parent_path = Path(file_path).parent
    Path(parent_path).mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, params=get_params)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch(launch_id: str = "latest") -> None:
    launch_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url=launch_url)
    response.raise_for_status()

    spacex_images = response.json()["links"]["flickr"]["original"]
    for i, image_url in enumerate(spacex_images):
        file_ext = get_url_file_extension(image_url)
        download_file(image_url, f"images/spacex{i}{file_ext}")


def get_url_file_extension(file_url: str) -> str:
    file_path = urlsplit(file_url).path
    path, file_name = split(file_path)
    name, extension = splitext(unquote(file_name))
    return extension


def fetch_nasa_apod(count: int = 30) -> None:
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count": count,
        "api_key": "q5rRNPnc7ejPUAnEXfGOXeaJsfSMxEVdpggKye6s",
    }
    response = requests.get(url=nasa_apod_url, params=payload)
    response.raise_for_status()
    for i, image in enumerate(response.json()):
        image_url = image["url"]
        image_ext = get_url_file_extension(image_url)
        download_file(image_url, f"images/nasa_apod{i}{image_ext}")


def fetch_nasa_epic() -> None:
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    nasa_epic_archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
    payload = {
        "api_key": "q5rRNPnc7ejPUAnEXfGOXeaJsfSMxEVdpggKye6s",
    }
    response = requests.get(url=nasa_epic_url, params=payload)
    response.raise_for_status()
    for i, image_metadata in enumerate(response.json()):
        if i < 5:
            image_datetime = datetime.datetime.fromisoformat(image_metadata["date"])
            image_url = f"{nasa_epic_archive_url}{image_datetime.strftime('%Y/%m/%d')}" \
                        f"/png/{image_metadata['image']}.png"
            download_file(image_url, f"images/nasa_epic{i}.png", get_params=payload)


if __name__ == "__main__":
    # "5eb87ce4ffd86e000604b337"
    # fetch_spacex_last_launch("5eb87ce4ffd86e000604b337")
    # fetch_nasa_apod(10)
    fetch_nasa_epic()
