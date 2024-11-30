# client.py

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize and return the bot client instance
def create_bot():
    return Client("media_info_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
