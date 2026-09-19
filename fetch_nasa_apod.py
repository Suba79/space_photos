import os

import requests
from dotenv import load_dotenv

from utils import get_file_extension


USER_AGENT = "space-photos-training-project/1.0"

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


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


def get_apod_images(api_key, count):
    params = {
        "api_key": api_key,
        "count": count,
    }

    try:
        response = requests.get(
            NASA_APOD_URL,
            params=params,
            proxies=PROXIES,
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
            proxies=PROXIES,
            timeout=30,
        )
        response.raise_for_status()

    apod_images = response.json()

    if isinstance(apod_images, dict):
        apod_images = [apod_images]

    return apod_images


def fetch_nasa_apod(api_key, count=40):
    os.makedirs("images", exist_ok=True)

    apod_images = get_apod_images(api_key, count)

    image_number = 1

    for apod_image in apod_images:
        if apod_image.get("media_type") != "image":
            continue

        image_url = apod_image["url"]
        extension = get_file_extension(image_url)

        image_path = f"images/nasa_apod_{image_number}{extension}"

        download_image(image_url, image_path)

        image_number += 1


load_dotenv()

nasa_api_key = os.environ["NASA_API_KEY"]

fetch_nasa_apod(nasa_api_key)