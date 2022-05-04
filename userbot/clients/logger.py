# Zed - UserBot
# Copyright (c) 2022 Zee-Userbot
# Credits: @Zed-Thon || https://github.com/Zed-Thon
#
# This file is a part of < https://github.com/Zed-Thon/Zee-Userbot/ >
# t.me/ZedThon & t.me/zzzzl1l

import asyncio

from telethon.tl.functions.channels import EditAdminRequest, InviteToChannelRequest
from telethon.tl.types import ChatAdminRights

from userbot import BOT_VER as version
from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import ZED2, ZED3, ZED4, ZED5, bot, branch, tgbot

MSG_ON = """
⚡ **تم تنصيب زدثـــون .. بنجـاح ✅**
━━
➠ **اصـدار السـورس -** `{}@{}`
➠ **ارسـل** `{}فحص` **للتحقق من التنصيب**
━━
"""


async def zed_userbot_on():
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    try:
        if bot and tgbot:
            ZeeUBOT = await tgbot.get_me()
            BOT_USERNAME = ZeeUBOT.username
            await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
            await asyncio.sleep(3)
    except BaseException:
        pass
    try:
        if bot and tgbot:
            ZeeUBOT = await tgbot.get_me()
            BOT_USERNAME = ZeeUBOT.username
            await bot(EditAdminRequest(BOTLOG_CHATID, BOT_USERNAME, new_rights, "BOT"))
            await asyncio.sleep(3)
    except BaseException:
        pass
    try:
        if bot:
            await checking(bot)
            await asyncio.sleep(3)
            if BOTLOG_CHATID != 0:
                await bot.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if ZED2:
            await checking(ZED2)
            await asyncio.sleep(3)
            if BOTLOG_CHATID != 0:
                await ZED2.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if ZED3:
            await checking(ZED3)
            await asyncio.sleep(3)
            if BOTLOG_CHATID != 0:
                await ZED3.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if ZED4:
            await checking(ZED4)
            await asyncio.sleep(3)
            if BOTLOG_CHATID != 0:
                await ZED4.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
    try:
        if ZED5:
            await checking(ZED5)
            await asyncio.sleep(3)
            if BOTLOG_CHATID != 0:
                await ZED5.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd),
                )
    except BaseException:
        pass
