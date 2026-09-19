import os
from urllib.parse import unquote, urlsplit

import requests


USER_AGENT = "space-photos-training-project/1.0"


def download_image(url, filepath, proxies=None):
    headers = {
        "User-Agent": USER_AGENT,
    }

    response = requests.get(
        url,
        proxies=proxies,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)


def get_file_extension(url):
    parsed_url = urlsplit(url)
    file_path = unquote(parsed_url.path)
    _, filename = os.path.split(file_path)
    _, extension = os.path.splitext(filename)

    return extension