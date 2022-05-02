# Credits: @ZedThon
# FROM ZeeUserbot <https://github.com/Zed-Thon/ZeeUserbot>
# t.me/ZedThon & t.me/zzzzl1l

import asyncio
import importlib
import logging
import sys
from pathlib import Path
from random import randint

import heroku3
from telethon.errors import (
    BotMethodInvalidError,
    ChannelPrivateError,
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id
from userbot import (
    BOT_TOKEN,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGS,
    bot,
)

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


async def autobot():
    if BOT_TOKEN:
        return
    await bot.start()
    await asyncio.sleep(15)
    await bot.send_message(
        BOTLOG_CHATID, "**- جـاري انشـاء البوت المسـاعد الخاص بك فـي @BotFather**"
    )
    LOGS.info("انتظر ثواني ... جـاري انشـاء البـوت المسـاعد الخـاص بك")
    who = await bot.get_me()
    name = f"{who.first_name} البـوت المسـاعد"
    if who.username:
        username = f"{who.username}_ubot"
    else:
        username = f"zed{(str(who.id))[5:]}ubot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "الرجاء انشـاء بوت من @BotFather وقم باضافـة التوكـن للفـار BOT_TOKEN"
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "البـوت المسـاعد زد")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "الرجاء انشـاء بوت من @BotFather وقم باضافـة التوكـن للفـار BOT_TOKEN"
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"zed{(str(who.id))[6:]}{str(ran)}ubot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_file(bf, "userbot/resources/logo.jpg")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(
                bf, f"🧑🏻‍💻 المستخـدم ~ {who.first_name} 🧑🏻‍💻\n\n🌐 قنـاة السـورس ~ @ZedThon 🌐"
            )
            await bot.send_message(
                BOTLOG_CHATID,
                f"**- تم بـ نجاح إنشاء بـوت مسـاعد خـاص بالمستخـدم  @{username}**",
            )
            LOGS.info(f"- تم بـ نجاح إنشاء بـوت مسـاعد خـاص بالمستخـدم  @{username}")
            await bot.send_message(
                BOTLOG_CHATID,
                "**- انتظر لحظة ، ثم قم بإعادة تشغيل اليدوي في Heroku لتطبيق التغييرات.**",
            )
            heroku_var["BOT_TOKEN"] = token
        else:
            LOGS.info(
                "يرجى حذف بعض بوتاتـك الموجودة على @Botfather واضف التوكن للفـار BOT_TOKEN "
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setuserpic")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_file(bf, "userbot/resources/logo.jpg")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(
            bf, f"🧑🏻‍💻 المستخـدم ~ {who.first_name} 🧑🏻‍💻\n\n🌐 قنـاة السـورس ~ @ZedThon 🌐"
        )
        await bot.send_message(
            BOTLOG_CHATID,
            f"**- تم بـ نجاح إنشاء بـوت مسـاعد خـاص بالمستخـدم  @{username}**",
        )
        LOGS.info(f"- تم بـ نجاح إنشاء بـوت مسـاعد خـاص بالمستخـدم  @{username}")
        await bot.send_message(
            BOTLOG_CHATID,
            "**انتظر لحضات ، ثم قم بإعادة التشغيل اليدوي في هيروكو لتطبيق التغييرات.**",
        )
        heroku_var["BOT_TOKEN"] = token
    else:
        LOGS.info(
            "يرجى حذف بعض بوتاتـك الموجودة على @Botfather واضف التوكن للفـار BOT_TOKEN "
        )
        sys.exit(1)

def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/modules/{shortname}.py")
        name = f"userbot.modules.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info(f"Successfully imported {shortname}")
    else:

        path = Path(f"userbot/modules/{shortname}.py")
        name = f"userbot.modules.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.LOGS = LOGS
        mod.CMD_HELP = CMD_HELP
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        # for imports
        sys.modules[f"userbot.modules.{shortname}"] = mod
        LOGS.info(f"Successfully imported {shortname}")


def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = f"userbot.modules.assistant.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Starting Your Assistant Bot.")
        LOGS.info(f"Assistant Sucessfully imported {shortname}")
    else:
        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = f"userbot.modules.assistant.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules[f"userbot.modules.assistant{shortname}"] = mod
        LOGS.info(f"Assistant Successfully imported{shortname}")


def remove_plugin(shortname):
    try:
        try:
            for i in CMD_HELP[shortname]:
                bot.remove_event_handler(i)
            del CMD_HELP[shortname]

        except BaseException:
            name = f"userbot.modules.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError
