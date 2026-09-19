import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.utils.request import Request


PROXY_URL = "socks5h://127.0.0.1:10808"


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

    bot.send_message(
        chat_id=telegram_channel_id,
        text="Hello from Space Photos!",
    )


if __name__ == "__main__":
    main()  