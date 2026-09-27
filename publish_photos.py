import argparse
import os
import random
import time

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request

from utils import get_image_paths, prepare_photo


DEFAULT_DELAY = 4 * 60 * 60
MAX_FILE_SIZE = 10 * 1024 * 1024


def publish_photo(bot, channel_id, image_path):
    photo = prepare_photo(image_path)

    try:
        bot.send_photo(
            chat_id=channel_id,
            photo=photo,
        )
    finally:
        photo.close()


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
    proxy_url = os.getenv("PROXY_URL")

    publish_delay = int(
        os.getenv(
            "PUBLISH_DELAY",
            DEFAULT_DELAY,
        )
    )

    request = Request(
        proxy_url=proxy_url,
        connect_timeout=30,
        read_timeout=30,
    )

    bot = Bot(
        token=telegram_bot_token,
        request=request,
    )

    image_paths = get_image_paths(
        args.directory,
        max_file_size=MAX_FILE_SIZE,
    )

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
