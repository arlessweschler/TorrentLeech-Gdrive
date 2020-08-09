#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
#

import asyncio
import math
import os
import time
import subprocess
from datetime import datetime
from pyrogram import Client, Filters
from pathlib import Path

from tobrot import (
    DOWNLOAD_LOCATION
)
from tobrot.helper_funcs.display_progress_g import progress_for_pyrogram_g
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function_t
from tobrot.helper_funcs.create_compressed_archive import unzip_me, unrar_me, untar_me

async def down_load_media_f(client, message):
    user_id = message.from_user.id
    print(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = DOWNLOAD_LOCATION + "/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram_g,
            progress_args=(
                "trying to download", mess_age, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        print(the_real_download_location)
        await asyncio.sleep(10)
        await mess_age.edit_text(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds")
        gk = subprocess.Popen(['mv', f'{the_real_download_location}', '/app/'], stdout = subprocess.PIPE)
        out = gk.communicate()
        the_real_download_location_g = os.path.basename(the_real_download_location)
        if len(message.command) > 1:
            if message.command[1] == "unzip":
                file_upload = await unzip_me(the_real_download_location_g)      
            elif message.command[1] == "unrar":
                file_upload = await unrar_me(the_real_download_location_g)      
            elif message.command[1] == "untar":
                 file_upload = await untar_me(the_real_download_location_g)
            elif message.command[1] == "renameToMsgText":
                if message.text is not None:
                    newFileName=os.path.join(DOWNLOAD_LOCATION,mess_age.text+Path(the_real_download_location_g).suffix)
                    os.rename(the_real_download_location_g,newFileName)
                    the_real_download_location_g=newFileName
                    await mess_age.edit_text(f"Renamed to <code>{the_real_download_location}</code>")

            if file_upload is not None:
                    g_response = await upload_to_gdrive(file_upload, mess_age, message, user_id)
                    LOGGER.info(g_response)
        else:
            gaut_response = await upload_to_gdrive(the_real_download_location_g, mess_age, message, user_id)
            LOGGER.info(gaut_response)
    else:
        #await asyncio.sleep(4)
        await mess_age.edit_text("Reply to a Telegram Media, to upload to the Cloud Drive.")
