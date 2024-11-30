# mediainfo.py

import os
import re
import aiohttp
import aiofiles
import subprocess
from os import path as ospath
from subprocess import CalledProcessError
from aiofiles.os import path as aiopath, mkdir, remove as aioremove
from config import MEDIAINFO_PATH


# Helper function to execute shell commands (like mediainfo)
def cmd_exec(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode()
    except CalledProcessError as e:
        return str(e.output.decode())


# Function to generate media information (using mediainfo)
async def gen_mediainfo(message, link=None, media=None, msg=None):
    temp_send = await message.reply("Generating MediaInfo...")
    output_file = None  # Initialize output_file to avoid UnboundLocalError

    try:
        # Create a folder to store media files temporarily
        path = MEDIAINFO_PATH
        if not await aiopath.isdir(path):
            await mkdir(path)

        # Handle download from a link
        if link:
            filename = re.search(".+/(.+)", link).group(1)
            des_path = ospath.join(path, filename)
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 12; 2201116PI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            }
            async with aiohttp.ClientSession() as session, session.get(link, headers=headers) as response:
                async with aiofiles.open(des_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(10000000):
                        await f.write(chunk)

        # Handle media sent directly to the bot
        elif media:
            des_path = ospath.join(path, media.file_name)
            if media.file_size <= 50000000:
                await msg.download(ospath.join(os.getcwd(), des_path))
            else:
                async for chunk in bot.stream_media(media, limit=5):
                    async with aiofiles.open(des_path, "ab") as f:
                        await f.write(chunk)

        # Execute mediainfo to get media details
        stdout = cmd_exec(f'mediainfo "{des_path}"')

        # Save the MediaInfo output to a text file
        output_file = ospath.join(path, f"{ospath.basename(des_path)}_mediainfo.txt")
        async with aiofiles.open(output_file, "w") as f:
            await f.write(stdout)

        # Send the file to the user
        await message.reply_document(output_file, caption=f"MediaInfo for {ospath.basename(des_path)}")

    except Exception as e:
        await message.reply(f"MediaInfo generation failed: {e}")
        return
    finally:
        # Clean up temporary files
        if os.path.exists(des_path):
            await aioremove(des_path)
        if output_file and os.path.exists(output_file):
            await aioremove(output_file)
