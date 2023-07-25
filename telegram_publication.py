#!/usr/bin/env python3
import argparse
import os
import random

from dotenv import load_dotenv

import telegram

import file_actions


def post_image(image_path: str) -> None:
    load_dotenv()
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    media = telegram.InputMediaPhoto(media=open(image_path, "rb"))
    bot.send_media_group(chat_id=os.getenv("TELEGRAM_CHAT_ID"), media=[media])


if __name__ == "__main__":
    images_directory = "images"
    image = random.choice(file_actions.get_all_files(images_directory))
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", help="Image path", default=image)
    args = parser.parse_args()
    post_image(args.image_path)
