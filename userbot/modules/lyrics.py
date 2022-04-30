# Copyright (C) 2022 Zed-Userbot
# Created by Zed-Thon
# FROM <https://github.com/Zed-Thon/Zee-Userbot>
# t.me/ZedThon & t.me/zzzzl1l

import requests

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, zed_cmd


@zed_cmd(pattern="lyrics(?:\s|$)([\s\S]*)")
async def _(event):
    query = event.pattern_match.group(1)
    if not query:
        return await edit_or_reply(event, "**Silahkan Masukan Judul Lagu**")
    try:
        xxnx = await edit_or_reply(event, "`Searching Lyrics...`")
        respond = requests.get(
            f"https://api-tede.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{respond['data']}"
        await xxnx.edit(result)
    except Exception:
        await xxnx.edit("**Lirik lagu tidak ditemukan.**")


CMD_HELP.update(
    {
        "lyrics": f"**Plugin : **`lyrics`\
        \n\n  •  **Syntax :** `{cmd}lyrics` <judul lagu>\
        \n  •  **Function : **Dapatkan lirik lagu yang cocok dengan judul lagu.\
    "
    }
)
