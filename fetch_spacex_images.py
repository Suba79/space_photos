import argparse
import os
import time

import requests
from dotenv import load_dotenv

from utils import download_image, get_proxies


USER_AGENT = "space-photos-training-project/1.0"
WIKIMEDIA_API_URL = "https://commons.wikimedia.org/w/api.php"
DEFAULT_SEARCH_QUERY = "Starlink 17-38"
DEFAULT_IMAGES_DIRECTORY = "images"
DEFAULT_ENV_FILE = ".env"


def fetch_spacex_images(search_query, directory, proxies=None):
    os.makedirs(directory, exist_ok=True)

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": search_query,
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "format": "json",
    }

    headers = {"User-Agent": USER_AGENT}

    response = requests.get(
        WIKIMEDIA_API_URL,
        params=params,
        proxies=proxies,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    pages = response.json()["query"]["pages"].values()
    image_urls = []

    for page in pages:
        image_info = page["imageinfo"][0]
        if image_info["mime"].startswith("image/"):
            image_urls.append(image_info["url"])

    for image_number, image_url in enumerate(image_urls, start=1):
        image_path = os.path.join(directory, f"spacex{image_number}.jpg")
        download_image(image_url, image_path, proxies=proxies)
        time.sleep(5)


def main():
    parser = argparse.ArgumentParser(
        description="Download SpaceX launch images from Wikimedia Commons."
    )
    parser.add_argument(
        "search_query",
        nargs="?",
        default=DEFAULT_SEARCH_QUERY,
        help="Search query for Wikimedia Commons.",
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

    fetch_spacex_images(
        args.search_query,
        directory=args.directory,
        proxies=get_proxies(),
    )


if __name__ == "__main__":
    main()
