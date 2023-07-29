#!/usr/bin/env python3
import argparse
import os
import random
from pathlib import Path

import telegram
from dotenv import load_dotenv

import telegram_publication
import time
import file_actions


if __name__ == "__main__":
    load_dotenv()
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]

    parser = argparse.ArgumentParser(description="Publication all images")
    parser.add_argument(
        "--publication_interval",
        help="Interval in hours",
        default=4,
        type=int
    )
    parser.add_argument(
        "--images_directory",
        help="Directory with images",
        default="images",
        type=Path
    )
    args = parser.parse_args()

    images_directory = args.images_directory

    files = file_actions.get_all_files(images_directory)

    while True:
        random.shuffle(files)
        for file in files:
            timeout_connection = 1
            error = True
            while error:
                try:
                    telegram_publication.post_image(telegram_bot_token, telegram_chat_id, file)
                except telegram.error.NetworkError:
                    time.sleep(timeout_connection)
                    timeout_connection = 5
                else:
                    error = False
                    time.sleep(60 * 60 * args.publication_interval)
