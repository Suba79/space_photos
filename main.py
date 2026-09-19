import os

import requests


def download_image(url, filepath):
    headers = {
        "User-Agent": "space-photos-training-project/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)


os.makedirs("images", exist_ok=True)

image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
image_path = "images/hubble.jpeg"

download_image(image_url, image_path)