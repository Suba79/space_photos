import argparse
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from utils import download_image, get_proxies


NASA_EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural"
DEFAULT_IMAGES_DIRECTORY = "images"
DEFAULT_ENV_FILE = ".env"


def get_epic_images(api_key, proxies=None):
    try:
        response = requests.get(
            NASA_EPIC_API_URL,
            params={"api_key": api_key},
            proxies=proxies,
            timeout=30,
        )
        response.raise_for_status()
        return response.json(), api_key
    except requests.exceptions.RequestException:
        demo_key = "DEMO_KEY"
        response = requests.get(
            NASA_EPIC_API_URL,
            params={"api_key": demo_key},
            proxies=proxies,
            timeout=30,
        )
        response.raise_for_status()
        return response.json(), demo_key


def fetch_nasa_epic(api_key, directory, images_count=10, proxies=None):
    os.makedirs(directory, exist_ok=True)
    epic_images, working_api_key = get_epic_images(
        api_key,
        proxies=proxies,
    )

    for image_number, epic_image in enumerate(
        epic_images[:images_count],
        start=1,
    ):
        image_name = epic_image["image"]
        image_date = datetime.strptime(
            epic_image["date"],
            "%Y-%m-%d %H:%M:%S",
        )

        image_url = (
            "https://api.nasa.gov/EPIC/archive/natural/"
            f"{image_date:%Y/%m/%d}/png/"
            f"{image_name}.png"
        )

        prepared_request = requests.Request(
            "GET",
            image_url,
            params={"api_key": working_api_key},
        ).prepare()

        image_path = os.path.join(
            directory,
            f"nasa_epic_{image_number}.png",
        )

        download_image(
            prepared_request.url,
            image_path,
            proxies=proxies,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Download NASA EPIC images."
    )
    parser.add_argument(
        "--directory",
        default=DEFAULT_IMAGES_DIRECTORY,
        help="Directory for downloaded images.",
    )
    parser.add_argument(
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help="Path to the environment file.",
    )

    args = parser.parse_args()
    load_dotenv(args.env_file)

    fetch_nasa_epic(
        os.environ["NASA_API_KEY"],
        directory=args.directory,
        proxies=get_proxies(),
    )


if __name__ == "__main__":
    main()
