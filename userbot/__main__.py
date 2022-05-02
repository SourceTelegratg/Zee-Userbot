# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Copyright (C) 2021 TeamUltroid for autobot
# Recode by @Zed-Thon
# FROM Zee-Userbot <https://github.com/Zed-Thon/Zee-Userbot>
# t.me/ZedThon & t.me/zzzzl1l
#
""" Userbot start point """


import sys
from importlib import import_module
from platform import python_version

from pytgcalls import __version__ as pytgcalls
from pytgcalls import idle
from telethon import version

from userbot import BOT_TOKEN
from userbot import BOT_VER as ubotversion
from userbot import BOTLOG_CHATID, LOGS, LOOP, bot
from userbot.clients import zed_userbot_on, multized
from userbot.core.git import git
from userbot.modules import ALL_MODULES
from userbot.utils import autobot

try:
    for module_name in ALL_MODULES:
        imported_module = import_module(f"userbot.modules.{module_name}")
    client = multized()
    total = 5 - client
    git()
    LOGS.info(f"عدد الجلسات = {total} جلسـه")
    LOGS.info(f"اصدار بايثون - {python_version()}")
    LOGS.info(f"اصدار تليثون - {version.__version__}")
    LOGS.info(f"اصدار مكتبة الاغاني - {pytgcalls.__version__}")
    LOGS.info(f"اصدار زدثــون - {ubotversion} [🔥 تم التنصيب .. بنجـاح✓ 🔥]")
except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
    pass
except BaseException as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)


LOOP.run_until_complete(zed_userbot_on())
if not BOT_TOKEN:
    LOOP.run_until_complete(autobot())
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    LOOP.run_until_disconnected()