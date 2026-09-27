import argparse
import os
import random

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request

from utils import get_image_paths, prepare_photo


IMAGES_DIRECTORY = "images"
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_random_image():
    image_paths = get_image_paths(
        IMAGES_DIRECTORY,
        max_file_size=MAX_FILE_SIZE,
    )

    if not image_paths:
        raise RuntimeError("No images found.")

    return random.choice(image_paths)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Publish a photo to Telegram channel."
    )

    parser.add_argument(
        "image",
        nargs="?",
        help="Path to image. If omitted, a random image is used.",
    )

    args = parser.parse_args()

    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_channel_id = os.environ["TELEGRAM_CHANNEL_ID"]
    proxy_url = os.getenv("PROXY_URL")

    request = Request(
        proxy_url=proxy_url,
        connect_timeout=30,
        read_timeout=30,
    )

    bot = Bot(
        token=telegram_bot_token,
        request=request,
    )

    if args.image:
        image_path = args.image
    else:
        image_path = get_random_image()

    if os.path.getsize(image_path) > MAX_FILE_SIZE:
        raise RuntimeError("Image is larger than 10 MB.")

    photo = prepare_photo(image_path)

    try:
        bot.send_photo(
            chat_id=telegram_channel_id,
            photo=photo,
        )
    finally:
        photo.close()


if __name__ == "__main__":
    main()
