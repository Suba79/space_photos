import argparse
import os
import random

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request

from utils import get_image_paths, prepare_photo


DEFAULT_IMAGES_DIRECTORY = "images"
DEFAULT_ENV_FILE = ".env"
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_random_image(directory):
    image_paths = get_image_paths(
        directory,
        max_file_size=MAX_FILE_SIZE,
    )

    if not image_paths:
        raise RuntimeError("No images found.")

    return random.choice(image_paths)


def main():
    parser = argparse.ArgumentParser(
        description="Publish a photo to Telegram channel."
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="Path to image. If omitted, a random image is used.",
    )
    parser.add_argument(
        "--directory",
        default=DEFAULT_IMAGES_DIRECTORY,
        help="Directory for random image selection.",
    )
    parser.add_argument(
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help="Path to the environment file.",
    )

    args = parser.parse_args()
    load_dotenv(args.env_file)

    request = Request(
        proxy_url=os.getenv("PROXY_URL"),
        connect_timeout=30,
        read_timeout=30,
    )

    bot = Bot(
        token=os.environ["TELEGRAM_BOT_TOKEN"],
        request=request,
    )

    image_path = args.image or get_random_image(args.directory)

    if os.path.getsize(image_path) > MAX_FILE_SIZE:
        raise RuntimeError("Image is larger than 10 MB.")

    photo = prepare_photo(image_path)

    try:
        bot.send_photo(
            chat_id=os.environ["TELEGRAM_CHANNEL_ID"],
            photo=photo,
        )
    finally:
        photo.close()


if __name__ == "__main__":
    main()
