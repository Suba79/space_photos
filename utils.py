import time
import io
import os
from urllib.parse import unquote, urlsplit

import requests
from PIL import Image


USER_AGENT = "space-photos-training-project/1.0"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}

MAX_DIMENSIONS_SUM = 9900


def get_proxies():
    proxy_url = os.getenv("PROXY_URL")

    if not proxy_url:
        return None

    return {
        "http": proxy_url,
        "https": proxy_url,
    }


def download_image(url, filepath, proxies=None):
    headers = {
        "User-Agent": USER_AGENT,
    }

    for attempt in range(3):
        response = requests.get(
            url,
            proxies=proxies,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 429:
            time.sleep(15 * (attempt + 1))
            continue

        response.raise_for_status()

        with open(filepath, "wb") as file:
            file.write(response.content)

        return

    response.raise_for_status()


def get_file_extension(url):
    parsed_url = urlsplit(url)
    file_path = unquote(parsed_url.path)
    _, filename = os.path.split(file_path)
    _, extension = os.path.splitext(filename)

    return extension


def get_image_paths(directory, max_file_size=None):
    image_paths = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if not os.path.isfile(filepath):
            continue

        _, extension = os.path.splitext(filename)

        if extension.lower() not in IMAGE_EXTENSIONS:
            continue

        if max_file_size and os.path.getsize(filepath) > max_file_size:
            continue

        image_paths.append(filepath)

    return image_paths


def prepare_photo(image_path):
    with Image.open(image_path) as image:
        width, height = image.size

        if width + height <= MAX_DIMENSIONS_SUM:
            return open(image_path, "rb")

        scale = MAX_DIMENSIONS_SUM / (width + height)

        new_width = int(width * scale)
        new_height = int(height * scale)

        resized_image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS,
        )

        _, extension = os.path.splitext(image_path)
        extension = extension.lower()

        photo = io.BytesIO()

        if extension in {".jpg", ".jpeg"}:
            if resized_image.mode != "RGB":
                resized_image = resized_image.convert("RGB")

            resized_image.save(
                photo,
                format="JPEG",
                quality=95,
            )

            photo.name = "photo.jpg"
        else:
            resized_image.save(
                photo,
                format="PNG",
            )

            photo.name = "photo.png"

        photo.seek(0)

        return photo
