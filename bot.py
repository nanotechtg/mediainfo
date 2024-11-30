# bot.py

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from config import API_ID, API_HASH, BOT_TOKEN
from mediainfo import gen_mediainfo


# Initialize Pyrogram client
bot = Client("media_info_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


# Command Handlers

# Start command handler: Sends welcome message and instructions
async def start(_, message: Message):
    start_message = (
        "Welcome to the MediaInfo bot! 🤖\n\n"
        "Send a media file or a download link to get detailed media information.\n"
        "Use the command `/mediainfo` to get info about media files or links.\n\n"
        "Example:\n"
        "- Send a media file: The bot will reply with information about the file.\n"
        "- Send a download link: The bot will fetch the file and provide details."
    )
    await message.reply(start_message)


# Mediainfo command handler: Generates media info based on user input
async def mediainfo(_, message: Message):
    reply = message.reply_to_message
    help_msg = (
        "<b>By replying to media:</b>"
        f"\n<code>/mediainfo media </code>"
        "\n\n<b>By sending download link:</b>"
        f"\n<code>/mediainfo link </code>"
    )
    # Check if the user provided a valid link or media
    if len(message.command) > 1 or (reply and reply.text):
        link = reply.text if reply else message.command[1]
        await gen_mediainfo(message, link=link)
    elif reply:
        if file := next(
            (i for i in [reply.document, reply.video, reply.audio] if i), None
        ):
            await gen_mediainfo(message, media=file, msg=reply)
        else:
            await message.reply(help_msg)
    else:
        await message.reply(help_msg)


# Add handlers for commands
bot.add_handler(MessageHandler(mediainfo, filters=filters.command("mediainfo")))
bot.add_handler(MessageHandler(start, filters=filters.command("start")))

# Run the bot
if __name__ == "__main__":
    bot.run()
