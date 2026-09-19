import os
import time

import requests


USER_AGENT = "space-photos-training-project/1.0"

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}


def download_image(url, filepath):
    headers = {
        "User-Agent": USER_AGENT,
    }

    response = requests.get(
        url,
        proxies=PROXIES,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    os.makedirs("images", exist_ok=True)

    api_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": "Starlink 17-38",
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
        api_url,
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

        download_image(image_url, image_path)
        time.sleep(5)


fetch_spacex_last_launch()