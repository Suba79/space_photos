import argparse
import os

import requests
from dotenv import load_dotenv

from utils import download_image, get_file_extension, get_proxies


NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
DEFAULT_IMAGES_DIRECTORY = "images"
DEFAULT_ENV_FILE = ".env"


def get_apod_images(api_key, count, proxies=None):
    response = requests.get(
        NASA_APOD_URL,
        params={
            "api_key": api_key,
            "count": count,
        },
        proxies=proxies,
        timeout=30,
    )
    response.raise_for_status()

    apod_images = response.json()

    if isinstance(apod_images, dict):
        apod_images = [apod_images]

    return apod_images


def fetch_nasa_apod(api_key, directory, count=40, proxies=None):
    os.makedirs(directory, exist_ok=True)

    apod_images = get_apod_images(
        api_key,
        count,
        proxies=proxies,
    )

    image_number = 1

    for apod_image in apod_images:
        if apod_image.get("media_type") != "image":
            continue

        image_url = apod_image["url"]
        extension = get_file_extension(image_url)

        image_path = os.path.join(
            directory,
            f"nasa_apod_{image_number}{extension}",
        )

        download_image(
            image_url,
            image_path,
            proxies=proxies,
        )

        image_number += 1


def main():
    parser = argparse.ArgumentParser(
        description="Download NASA APOD images."
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

    fetch_nasa_apod(
        os.environ["NASA_API_KEY"],
        directory=args.directory,
        proxies=get_proxies(),
    )


if __name__ == "__main__":
    main()
