import argparse
import os
import time

import requests

from utils import download_image


PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}

USER_AGENT = "space-photos-training-project/1.0"
WIKIMEDIA_API_URL = "https://commons.wikimedia.org/w/api.php"

DEFAULT_SEARCH_QUERY = "Starlink 17-38"


def fetch_spacex_images(search_query):
    os.makedirs("images", exist_ok=True)

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

    headers = {
        "User-Agent": USER_AGENT,
    }

    response = requests.get(
        WIKIMEDIA_API_URL,
        params=params,
        proxies=PROXIES,
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
        image_path = f"images/spacex{image_number}.jpg"

        download_image(
            image_url,
            image_path,
            proxies=PROXIES,
        )

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

    args = parser.parse_args()

    fetch_spacex_images(args.search_query)


if __name__ == "__main__":
    main()