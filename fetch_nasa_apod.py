import os

import requests
from dotenv import load_dotenv

from utils import download_image, get_file_extension, get_proxies


NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


def get_apod_images(api_key, count, proxies=None):
    params = {
        "api_key": api_key,
        "count": count,
    }

    try:
        response = requests.get(
            NASA_APOD_URL,
            params=params,
            proxies=proxies,
            timeout=30,
        )
        response.raise_for_status()

    except requests.exceptions.RequestException:
        fallback_params = {
            "api_key": "DEMO_KEY",
            "count": 1,
        }

        response = requests.get(
            NASA_APOD_URL,
            params=fallback_params,
            proxies=proxies,
            timeout=30,
        )
        response.raise_for_status()

    apod_images = response.json()

    if isinstance(apod_images, dict):
        apod_images = [apod_images]

    return apod_images


def fetch_nasa_apod(api_key, count=40, proxies=None):
    os.makedirs("images", exist_ok=True)

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

        image_path = f"images/nasa_apod_{image_number}{extension}"

        try:
            download_image(
                image_url,
                image_path,
                proxies=proxies,
            )
        except requests.exceptions.RequestException:
            continue

        image_number += 1


def main():
    load_dotenv()

    nasa_api_key = os.environ["NASA_API_KEY"]
    proxies = get_proxies()

    fetch_nasa_apod(
        nasa_api_key,
        proxies=proxies,
    )


if __name__ == "__main__":
    main()
