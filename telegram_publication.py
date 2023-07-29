#!/usr/bin/env python3
import argparse
import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv

import telegram

import file_actions


def post_image(token: str, chat_id: str, image_path: Path) -> None:
    bot = telegram.Bot(token=token)
    with open(image_path, "rb") as file:
        media = telegram.InputMediaPhoto(media=file)
    bot.send_media_group(chat_id=chat_id, media=[media])


if __name__ == "__main__":
    load_dotenv()
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--images_directory",
        help="Directory with images",
        default="images",
        type=Path
    )
    args = parser.parse_known_args()[0]

    images_directory = args.images_directory
    image = random.choice(file_actions.get_all_files(images_directory))
    parser.add_argument(
        "--image_path",
        help="Image path",
        default=image,
        type=Path
    )
    args = parser.parse_args()

    if not args.image_path.is_file():
        sys.exit("Invalid file")
    post_image(telegram_bot_token, telegram_chat_id, args.image_path)
