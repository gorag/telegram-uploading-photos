import telegram


if __name__ == "__main__":
    # "5eb87ce4ffd86e000604b337"
    bot = telegram.Bot(token="6523902154:AAEd6Q_ijplmRVPlZvbuaYBQx3cHrLFBrCw")
    media = telegram.InputMediaPhoto(media=open("images/nasa_epic0.png", "rb"))
    bot.send_media_group(chat_id="@astronomy_df", media=[media])
