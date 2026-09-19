import os
from datetime import datetime

import requests
from dotenv import load_dotenv


USER_AGENT = "space-photos-training-project/1.0"

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}

NASA_EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural"


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


def get_epic_images(api_key):
    params = {
        "api_key": api_key,
    }

    try:
        response = requests.get(
            NASA_EPIC_API_URL,
            params=params,
            proxies=PROXIES,
            timeout=30,
        )
        response.raise_for_status()

        return response.json(), api_key

    except requests.exceptions.RequestException:
        demo_key = "DEMO_KEY"

        response = requests.get(
            NASA_EPIC_API_URL,
            params={"api_key": demo_key},
            proxies=PROXIES,
            timeout=30,
        )
        response.raise_for_status()

        return response.json(), demo_key


def fetch_nasa_epic(api_key, images_count=10):
    os.makedirs("images", exist_ok=True)

    epic_images, working_api_key = get_epic_images(api_key)

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

        params = {
            "api_key": working_api_key,
        }

        response = requests.Request(
            "GET",
            image_url,
            params=params,
        ).prepare()

        image_path = f"images/nasa_epic_{image_number}.png"

        download_image(response.url, image_path)


load_dotenv()

nasa_api_key = os.environ["NASA_API_KEY"]

fetch_nasa_epic(nasa_api_key)