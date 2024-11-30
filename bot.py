# bot.py

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from mediainfo import gen_mediainfo  # Import the media info generation function

# Configuration for the bot
API_ID = "9311834"  # Replace with your API ID
API_HASH = "bb92ce8a66904f227f332bd4e5a75623"  # Replace with your API hash
BOT_TOKEN = "7535237196:AAFg8B3ifmFstifOxE2gnJJu4NZTFAuVYPE"  # Replace with your bot token

# Create and configure the bot instance
bot = Client("media_info_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Function to handle the /start command
async def start(_, message):
    start_message = (
        "Welcome to the MediaInfo bot! 🤖\n\n"
        "Send a media file or a download link to get detailed media information.\n"
        "Use the command `/mediainfo` to get info about media files or links.\n\n"
        "Example:\n"
        "- Send a media file: The bot will reply with information about the file.\n"
        "- Send a download link: The bot will fetch the file and provide details."
    )
    await message.reply(start_message)

# Function to handle /mediainfo command
async def mediainfo(_, message):
    reply = message.reply_to_message
    help_msg = (
        "<b>By replying to media:</b>"
        f"\n<code>/mediainfo media </code>"
        "\n\n<b>By sending download link:</b>"
        f"\n<code>/mediainfo link </code>"
    )
    
    # Ensure there's media or a link to process
    if len(message.command) > 1 or (reply and reply.text):
        link = reply.text if reply else message.command[1]
        await gen_mediainfo(message, link=link, bot=bot)  # Pass bot to gen_mediainfo
    elif reply:
        if file := next(
            (i for i in [reply.document, reply.video, reply.audio] if i), None
        ):
            await gen_mediainfo(message, media=file, msg=reply, bot=bot)  # Pass bot to gen_mediainfo
        else:
            await message.reply(help_msg)
    else:
        await message.reply(help_msg)

# Add handlers for commands
bot.add_handler(MessageHandler(mediainfo, filters=filters.command("mediainfo")))
bot.add_handler(MessageHandler(start, filters=filters.command("start")))

# Function to run the bot
def run_bot():
    bot.run()

if __name__ == "__main__":
    run_bot()
