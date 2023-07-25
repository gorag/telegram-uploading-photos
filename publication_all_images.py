#!/usr/bin/env python3
import argparse
import random
import telegram_publication
import time
import file_actions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publication all images")
    parser.add_argument("--publication_interval", help="Interval in hours", default=4)
    args = parser.parse_args()
    images_directory = "images"
    files = file_actions.get_all_files(images_directory)
    while True:
        random.shuffle(files)
        for file in files:
            telegram_publication.post_image(file)
            time.sleep(60 * 60 * args.publication_interval)
