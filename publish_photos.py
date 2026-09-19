import argparse
import os
import random
import time

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request


PROXY_URL = "socks5h://127.0.0.1:10808"
DEFAULT_DELAY = 4 * 60 * 60
MAX_FILE_SIZE = 20 * 1024 * 1024

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def get_image_paths(directory):
    image_paths = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if not os.path.isfile(filepath):
            continue

        _, extension = os.path.splitext(filename)

        if extension.lower() not in IMAGE_EXTENSIONS:
            continue

        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            continue

        image_paths.append(filepath)

    return image_paths


def publish_photo(bot, channel_id, image_path):
    with open(image_path, "rb") as photo:
        bot.send_photo(
            chat_id=channel_id,
            photo=photo,
        )


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Publish photos to Telegram channel."
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default="images",
        help="Directory with photos.",
    )

    args = parser.parse_args()

    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_channel_id = os.environ["TELEGRAM_CHANNEL_ID"]

    publish_delay = int(
        os.getenv(
            "PUBLISH_DELAY",
            DEFAULT_DELAY,
        )
    )

    request = Request(
        proxy_url=PROXY_URL,
        connect_timeout=30,
        read_timeout=30,
    )

    bot = Bot(
        token=telegram_bot_token,
        request=request,
    )

    image_paths = get_image_paths(args.directory)

    if not image_paths:
        raise RuntimeError("No images found.")

    while True:
        random.shuffle(image_paths)

        for image_path in image_paths:
            publish_photo(
                bot,
                telegram_channel_id,
                image_path,
            )

            time.sleep(publish_delay)


if __name__ == "__main__":
    main()