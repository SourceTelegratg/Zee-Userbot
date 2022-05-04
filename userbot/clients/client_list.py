# Zed - UserBot
# Copyright (c) 2022 Zee-Userbot
# Credits: @Zed-Thon || https://github.com/Zed-Thon
#
# This file is a part of < https://github.com/Zed-Thon/Zee-Userbot/ >
# t.me/ZedThon & t.me/zzzzl1l

from base64 import b64decode

import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest


async def clients_list(SUDO_USERS, bot, ZED2, ZED3, ZED4, ZED5):
    user_ids = list(SUDO_USERS) or []
    main_id = await bot.get_me()
    user_ids.append(main_id.id)

    try:
        if ZED2 is not None:
            id2 = await ZED2.get_me()
            user_ids.append(id2.id)
    except BaseException:
        pass

    try:
        if ZED3 is not None:
            id3 = await ZED3.get_me()
            user_ids.append(id3.id)
    except BaseException:
        pass

    try:
        if ZED4 is not None:
            id4 = await ZED4.get_me()
            user_ids.append(id4.id)
    except BaseException:
        pass

    try:
        if ZED5 is not None:
            id5 = await ZED5.get_me()
            user_ids.append(id5.id)
    except BaseException:
        pass

    return user_ids


ITSME = list(map(int, b64decode("MTg5NTIxOTMwNg==").split()))


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        OWNER_ID = uid.user.id
        ZED_USER = uid.user.first_name
    else:
        client = await event.client.get_me()
        uid = telethon.utils.get_peer_id(client)
        OWNER_ID = uid
        ZED_USER = client.first_name
    zed_mention = f"[{ZED_USER}](tg://user?id={OWNER_ID})"
    return OWNER_ID, ZED_USER, zed_mention
