import os
import random

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request


PROXY_URL = "socks5h://127.0.0.1:10808"
IMAGES_DIRECTORY = "images"


def main():
    load_dotenv()

    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_channel_id = os.environ["TELEGRAM_CHANNEL_ID"]

    request = Request(
        proxy_url=PROXY_URL,
        connect_timeout=30,
        read_timeout=30,
    )

    bot = Bot(
        token=telegram_bot_token,
        request=request,
    )

    image_names = os.listdir(IMAGES_DIRECTORY)
    image_name = random.choice(image_names)
    image_path = os.path.join(IMAGES_DIRECTORY, image_name)

    with open(image_path, "rb") as photo:
        bot.send_photo(
            chat_id=telegram_channel_id,
            photo=photo,
        )


if __name__ == "__main__":
    main()