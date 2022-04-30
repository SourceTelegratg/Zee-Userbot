# Zed - UserBot
# Copyright (c) 2022 Zee-Userbot
# Credits: @Zed-Thon || https://github.com/Zed-Thon
#
# This file is a part of < https://github.com/Zed-Thon/Zee-Userbot/ >
# t.me/ZedThon & t.me/zzzzl1l

import sys

import telethon.utils

from userbot import BOT_VER as version
from userbot import (
    DEFAULT,
    DEVS,
    LOGS,
    ZED2,
    ZED3,
    ZED4,
    ZED5,
    STRING_2,
    STRING_3,
    STRING_4,
    STRING_5,
    STRING_SESSION,
    blacklistzed,
    bot,
    call_py,
)
from userbot.modules.gcast import GCAST_BLACKLIST as GBL

EOL = "EOL\nZee-UserBot v{}, Copyright © 2021-2022 ZelZal• <https://github.com/Zed-Thon>"
MSG_BLACKLIST = "SO DON'T HAVE TO ACTUALLY STOP, USERBOT {} I'M TURN OFF VERY.\nZee-UserBot v{}, Copyright © 2021-2022 Zed-Thon• <https://github.com/Zed-Thon>"


async def zed_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def multized():
    if 1895219306 not in DEVS:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if -1001473548283 not in GBL:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if 1895219306 not in DEFAULT:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    failed = 0
    if STRING_SESSION:
        try:
            bot.start()
            call_py.start()
            bot.loop.run_until_complete(zed_client(bot))
            user = bot.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(
                f"STRING_SESSION detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——"
            )
            if user.id in blacklistzed:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e), exc_info=True)

    if STRING_2:
        try:
            ZED2.start()
            ZED2.loop.run_until_complete(zed_client(ZED2))
            user = ZED2.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_2 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistzed:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e), exc_info=True)

    if STRING_3:
        try:
            ZED3.start()
            ZED3.loop.run_until_complete(zed_client(ZED3))
            user = ZED3.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_3 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistzed:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e), exc_info=True)

    if STRING_4:
        try:
            ZED4.start()
            ZED4.loop.run_until_complete(zed_client(ZED4))
            user = ZED4.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_4 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistzed:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e), exc_info=True)

    if STRING_5:
        try:
            ZED5.start()
            ZED5.loop.run_until_complete(zed_client(ZED5))
            user = ZED5.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_5 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistzed:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e), exc_info=True)

    if not STRING_SESSION:
        failed += 1
    if not STRING_2:
        failed += 1
    if not STRING_3:
        failed += 1
    if not STRING_4:
        failed += 1
    if not STRING_5:
        failed += 1
    return failed
