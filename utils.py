import os
from urllib.parse import unquote, urlsplit


def get_file_extension(url):
    parsed_url = urlsplit(url)
    file_path = unquote(parsed_url.path)
    _, filename = os.path.split(file_path)
    _, extension = os.path.splitext(filename)

    return extension