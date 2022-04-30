# Copyright (C) 2020 Catuserbot <https://github.com/sandy1709/catuserbot>
# Copyright (C) 2021 TeamUltroid <https://github.com/TeamUltroid/Ultroid>
# Recode by @ZedThon
# FROM Zee-Userbot <https://github.com/Zed-Thon/Zee-Userbot>
# t.me/ZedThon & t.me/zzzzl1l

import io
import re
import time
from datetime import datetime
from os import remove

import heroku3
from telegraph import Telegraph, upload_file
from telethon import Button, custom, events
from telethon.tl import types
from telethon.tl.types import MessageMediaWebPage
from telethon.utils import get_display_name, pack_bot_file_id

from userbot import (
    BOTLOG_CHATID,
    CHANNEL,
    CMD_HANDLER,
    GROUP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    SUDO_HANDLER,
    StartTime,
    tgbot,
    user,
)
from userbot.modules.sql_helper.bot_blacklists import check_is_black_list
from userbot.modules.sql_helper.bot_starters import (
    add_starter_to_db,
    get_all_starters,
    get_starter_details,
)
from userbot.modules.sql_helper.globals import gvarstatus
from userbot.utils import _format, asst_cmd, callback, reply_id

from .ping import get_readable_time

OWNER = user.first_name
OWNER_ID = user.id
telegraph = Telegraph()
r = telegraph.create_account(short_name="telegraph")
auth_url = r["auth_url"]


heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


async def setit(event, name, value):
    try:
        heroku_var[name] = value
    except BaseException:
        return await event.edit("**Maaf Gagal Menyimpan Karena ERROR**")


def text_to_url(event):
    if isinstance(event.media, MessageMediaWebPage):
        webpage = event.media.webpage
        if not isinstance(webpage, types.WebPageEmpty) and webpage.type in ["photo"]:
            return webpage.display_url
    return event.text


def get_back_button(name):
    return [Button.inline("« رجـوع", data=f"{name}")]


async def check_bot_started_users(user, event):
    if user.id == OWNER_ID:
        return
    check = get_starter_details(user.id)
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"🔮 **#BOT_START**\n**First Name:** {_format.mentionuser(user.first_name , user.id)} \
                \n**User ID: **`{user.id}`\
                \n**Action: **Telah Memulai saya."
    else:
        start_date = check.date
        notification = f"🔮 **#BOT_RESTART**\n**First Name:** {_format.mentionuser(user.first_name , user.id)}\
                \n**ID: **`{user.id}`\
                \n**Action: **Telah Me-Restart saya"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if BOTLOG_CHATID:
        await event.client.send_message(BOTLOG_CHATID, notification)


@callback(data=re.compile(b"pmclose"))
async def pmclose(event):
    if event.query.user_id == OWNER_ID:
        await event.delete()


@callback(data=re.compile(b"pmbot"))
async def pmbot(event):
    await event.delete()
    ZeeUBOT = await tgbot.get_me()
    botusername = ZeeUBOT.username
    if event.query.user_id == OWNER_ID:
        await tgbot.send_message(
            event.chat_id,
            message=f"""**قائمـة اوامـر خـاص البـوت المساعـد الخـاص بـك هي:**\n**ملاحظـه: هذا الأوامـر تعمـل فقـط بخـاص البـوت @{botusername}**\n\n• **الاوامـر : **/كشف <بالـرد ع رسـالة الشخص> • **الوصـف : **للعثور على معلومات مرسل الرسالة.\n• **الامـر : **/حظر <السبب> او /حظر <المعرف/الايدي> <السبب>\n• **الوصـف : **لحظر مستخدم من البـوت. (استخدم السبب عند الحظر)\n\n• **الامـر : **/الغاء حظر <السبب> أو /الغاء حظر + <المعرف/الايدي>\n• **الوصـف : **الغاء حظر المحظورين من البوت ، حتى يتمكنوا من إرسال رسائل إلى البوت مرة أخرى.\n• **ملاحظـه : **لجلب قائمة بـ المستخدمين المحظورين من البوت ارسل الامر`.المحظورون`\n\n• **الامـر : **/اذاعه\n• **الوصـف : **قم بالـرد على الرسالة ليتم اذاعتها لكل مشتركين البوت الخاص بك. للحصول على قائمة المشتركين ارسل الامر `.المشتركين`\n• **ملاحظـه : ** إذا قام المستخدم بـ حظر البوت ، فسيتم إزالته من قاعدة البيانات الخاصة بك ، أي سيتم إزالته من قائمة مشتركين البوت""",
            buttons=[
                [
                    custom.Button.inline(
                        "« رجـوع",
                        data="settings",
                    )
                ],
            ],
        )


@callback(data=re.compile(b"users"))
async def users(event):
    await event.delete()
    if event.query.user_id == OWNER_ID:
        total_users = get_all_starters()
        msg = "- قائمـة مشتـركين البـوت :\n\n"
        for user in total_users:
            msg += f"• الاسـم: {user.first_name}\n• الايـدي: {user.user_id}\n• تاريـخ الاشتـراك: {user.date}\n\n"
        with io.BytesIO(str.encode(msg)) as fileuser:
            fileuser.name = "listusers.txt"
            await tgbot.send_file(
                event.chat_id,
                fileuser,
                force_document=True,
                thumb="userbot/resources/logo.jpg",
                caption="**Total Pengguna Di Bot anda.**",
                allow_cache=False,
                buttons=[
                    (
                        Button.inline("« رجـوع", data="settings"),
                        Button.inline("اغـلاق", data="pmclose"),
                    )
                ],
            )


@callback(data=re.compile(b"settings"))
async def botsettings(event):
    await event.delete()
    if event.query.user_id == OWNER_ID:
        await tgbot.send_message(
            event.chat_id,
            message=f"**⎆┊مرحبـاً مطـوري  [{OWNER}](tg://user?id={OWNER_ID})**\n**⎆┊استخـدم ازرار التحـكم والمسـاعده بالاسفـل 🕹**",
            buttons=[
                (Button.inline("الفـارات", data="apiset"),),
                (
                    Button.inline("اوامـر البـوت", data="pmbot"),
                    Button.inline("المشتـركين", data="users"),
                ),
                (
                    Button.inline("البنـك", data="pingbot"),
                    Button.inline("وقت التشغيـل", data="uptimebot"),
                ),
                (Button.inline("اغـلاق", data="pmclose"),),
            ],
        )


@callback(data=re.compile(b"apiset"))
async def apiset(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [Button.inline("جلسـات متعـدده", data="multiclient")],
            [
                Button.inline("الصـور", data="alivemenu"),
                Button.inline("اكـواد خاصـه", data="apikeys"),
            ],
            [
                Button.inline("رمـز الاوامـر", data="hndlrmenu"),
                Button.inline("الانـلايـن", data="inlinemenu"),
            ],
            [Button.inline("« رجـوع", data="settings")],
        ],
    )


@callback(data=re.compile(b"apikeys"))
async def apikeys(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [
                Button.inline("ʙɪᴛʟʏ ᴛᴏᴋᴇɴ", data="btly"),
                Button.inline("ᴅᴇᴇᴢᴇʀ ᴀʀʟ ᴛᴏᴋᴇɴ", data="dzrl"),
            ],
            [
                Button.inline("ᴅᴇᴇᴘ ᴀᴘɪ", data="dapi"),
                Button.inline("ᴏᴄʀ ᴀᴘɪ", data="ocrapi"),
            ],
            [
                Button.inline("ᴏᴘᴇɴ ᴡᴇᴀᴛʜᴇʀ", data="opnwth"),
                Button.inline("ʀᴇᴍᴏᴠᴇ.ʙɢ ᴀᴘɪ", data="rmbgapi"),
            ],
            [Button.inline("« رجـوع", data="apiset")],
        ],
    )


@callback(data=re.compile(b"alivemenu"))
async def alivemenu(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [
                Button.inline("صـورة الفحص", data="alvlogo"),
            ],
            [
                Button.inline("ايموجي الفحص", data="alvmoji"),
                Button.inline("كليشـة الفحص", data="alvteks"),
            ],
            [
                Button.inline("- قنـاة البـوت", data="alvch"),
                Button.inline("- مطـور البـوت", data="alvgc"),
            ],
            [Button.inline("« رجـوع", data="apiset")],
        ],
    )


@callback(data=re.compile(b"hndlrmenu"))
async def hndlrmenu(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [
                Button.inline("الخاص بك", data="cmdhndlr"),
                Button.inline("الخاص بالمطور", data="sdhndlr"),
            ],
            [Button.inline("« رجـوع", data="apiset")],
        ],
    )


@callback(data=re.compile(b"multiclient"))
async def menuclient(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [
                Button.inline("الجلسـه الاسـاسيـه", data="strone"),
            ],
            [
                Button.inline("الجلسـه 2", data="strtwo"),
                Button.inline("الجـلسه 3", data="strtri"),
            ],
            [
                Button.inline("الجلسـه 4", data="strfor"),
                Button.inline("الجلسـه 5", data="strfiv"),
            ],
            [Button.inline("« رجـوع", data="apiset")],
        ],
    )


@callback(data=re.compile(b"inlinemenu"))
async def inlinemenu(event):
    await event.edit(
        "**- الرجـاء تحديد الفـار الـذي تريـد تغييـره**",
        buttons=[
            [
                Button.inline("ايموجي الانلاين", data="inmoji"),
                Button.inline("صورة الانلاين", data="inpics"),
            ],
            [Button.inline("« رجـوع", data="apiset")],
        ],
    )


@callback(data=re.compile(b"alvlogo"))
async def alvlogo(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_LOGO"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan Foto Untuk var {var} anda**\n\n- او اضغـط /cancel للإلغـاء.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message(
                    f"Membatalkan Proses Settings VAR {var}",
                    buttons=get_back_button("alivemenu"),
                )
        except BaseException:
            pass
        if (
            not (response.text).startswith("/")
            and response.text != ""
            and (not response.media or isinstance(response.media, MessageMediaWebPage))
        ):
            url = text_to_url(response)
        elif response.sticker:
            url = response.file.id
        else:
            media = await event.client.download_media(response, "alvpc")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                remove(media)
            except BaseException:
                return await conv.send_message(
                    f"**Maaf Gagal Mengganti Foto Untuk {var}**",
                    buttons=get_back_button("alivemenu"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"**{var} Berhasil di Ganti**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("alivemenu"),
        )


@callback(data=re.compile(b"alvmoji"))
async def alvmoji(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_EMOJI"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Emoji Untuk var ALIVE_EMOJI anda**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("alivemenu"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**ALIVE_EMOJI Berhasil di Ganti Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("alivemenu"),
        )


@callback(data=re.compile(b"alvteks"))
async def alvteks(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_TEKS_CUSTOM"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Teks Untuk var ALIVE_TEKS_CUSTOM anda**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("alivemenu"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**ALIVE_TEKS_CUSTOM Berhasil di Ganti Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("alivemenu"),
        )


@callback(data=re.compile(b"alvch"))
async def alvch(event):
    await event.delete()
    pru = event.sender_id
    var = "CHANNEL"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Username CHANNEL anda, Jangan Pakai @**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("alivemenu"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**Link CHANNEL Berhasil di Ganti Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("alivemenu"),
        )


@callback(data=re.compile(b"alvgc"))
async def alvgc(event):
    await event.delete()
    pru = event.sender_id
    var = "GROUP"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Username GROUP anda, Jangan Pakai @**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("alivemenu"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**Link GROUP Berhasil di Ganti Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("alivemenu"),
        )


@callback(data=re.compile(b"inmoji"))
async def inmoji(event):
    await event.delete()
    pru = event.sender_id
    var = "INLINE_EMOJI"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Teks Untuk var INLINE_EMOJI anda**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("inlinemenu"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**INLINE_EMOJI Berhasil di Ganti Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("inlinemenu"),
        )


@callback(data=re.compile(b"inpics"))
async def inpics(event):
    await event.delete()
    pru = event.sender_id
    var = "INLINE_PIC"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan Foto Untuk var {var} anda**\n\n- او اضغـط /cancel للإلغـاء.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message(
                    f"Membatalkan Proses Settings VAR {var}",
                    buttons=get_back_button("alivemenu"),
                )
        except BaseException:
            pass
        if (
            not (response.text).startswith("/")
            and response.text != ""
            and (not response.media or isinstance(response.media, MessageMediaWebPage))
        ):
            url = text_to_url(response)
        elif response.sticker:
            url = response.file.id
        else:
            media = await event.client.download_media(response, "inlpc")
            try:
                x = upload_file(media)
                url = f"https://telegra.ph/{x[0]}"
                remove(media)
            except BaseException:
                return await conv.send_message(
                    f"**Maaf Gagal Mengganti Foto Untuk {var}**",
                    buttons=get_back_button("inlinemenu"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"**{var} Berhasil di Ganti**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("inlinemenu"),
        )


@callback(data=re.compile(b"cmdhndlr"))
async def cmdhndlr(event):
    await event.delete()
    pru = event.sender_id
    var = "CMD_HANDLER"
    name = "CMD Handler/ Trigger"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Kirim Simbol yang anda inginkan sebagai Handler/Pemicu untuk menggunakan bot\nPenangan Anda Saat Ini adalah** [ `{CMD_HANDLER}` ]\n\n- او اضغـط /cancel للإلغـاء.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("hndlrmenu"),
            )
        elif len(themssg) > 1:
            await conv.send_message(
                "Handler yang anda masukan salah harap gunakan simbol",
                buttons=get_back_button("hndlrmenu"),
            )
        elif themssg.startswith(("/", "#", "@")):
            await conv.send_message(
                "Simbol ini tidak dapat digunakan sebagai handler, Silahkan Gunakan Simbol lain",
                buttons=get_back_button("hndlrmenu"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} **Berhasil diganti Menjadi** `{themssg}`",
                buttons=get_back_button("hndlrmenu"),
            )


@callback(data=re.compile(b"sdhndlr"))
async def sdhndlr(event):
    await event.delete()
    pru = event.sender_id
    var = "SUDO_HANDLER"
    name = "SUDO Handler/ Trigger"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Kirim Simbol yang anda inginkan sebagai HANDLER untuk pengguna sudo bot anda\nSUDO_HANDLER anda Saat Ini adalah** [ `{SUDO_HANDLER}` ]\n\n- او اضغـط /cancel للإلغـاء.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("hndlrmenu"),
            )
        elif len(themssg) > 1:
            await conv.send_message(
                "Handler yang anda masukan salah harap gunakan simbol",
                buttons=get_back_button("hndlrmenu"),
            )
        elif themssg.startswith(("/", "#", "@")):
            await conv.send_message(
                "Simbol ini tidak dapat digunakan sebagai handler, Silahkan Gunakan Simbol lain",
                buttons=get_back_button("hndlrmenu"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} **Berhasil diganti Menjadi** `{themssg}`",
                buttons=get_back_button("hndlrmenu"),
            )


@callback(data=re.compile(b"rmbgapi"))
async def rmbgapi(event):
    await event.delete()
    pru = event.sender_id
    var = "REM_BG_API_KEY"
    name = "Remove.bg API Key"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Silahkan Kirimkan Remove.bg API key Anda dari remove.bg**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apikeys"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"{name} **Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apikeys"),
        )


@callback(data=re.compile(b"dapi"))
async def deepai(event):
    await event.delete()
    pru = event.sender_id
    var = "DEEP_AI"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan API {var} Anda dari deepai.org**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apikeys"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apikeys"),
        )


@callback(data=re.compile(b"ocrapi"))
async def ocrapi(event):
    await event.delete()
    pru = event.sender_id
    var = "OCR_SPACE_API_KEY"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan {var} anda dari ocr.space**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apikeys"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apikeys"),
        )


@callback(data=re.compile(b"dzrl"))
async def dzrl(event):
    await event.delete()
    pru = event.sender_id
    var = "DEEZER_ARL_TOKEN"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan {var} anda dari developers.deezer.com**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apikeys"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apikeys"),
        )


@callback(data=re.compile(b"opnwth"))
async def opnwth(event):
    await event.delete()
    pru = event.sender_id
    var = "OPEN_WEATHER_MAP_APPID"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan {var} anda dari api.openweathermap.org/data/2.5/weather**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apikeys"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apikeys"),
        )


@callback(data=re.compile(b"btly"))
async def btly(event):
    await event.delete()
    pru = event.sender_id
    var = "BITLY_TOKEN"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**Silahkan Kirimkan {var} anda dari bitly.com**\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("apiset"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil di Setting Menjadi** `{themssg}`\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("apiset"),
        )


@callback(data=re.compile(b"strone"))
async def strone(event):
    await event.delete()
    pru = event.sender_id
    var = "STRING_SESSION"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**- قـم بالذهاب الى @Zedthonnbot  وإرسال كـود تيرمكـس هنـا لتسجيل جلسـه اضافيـه اخـرى {var} **\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {var}",
                buttons=get_back_button("multiclient"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{var} Berhasil diganti**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("multiclient"),
        )


@callback(data=re.compile(b"strtwo"))
async def strtwo(event):
    await event.delete()
    pru = event.sender_id
    var = "STRING_2"
    name = "MULTI CLIENT ke 2"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**- قـم بالذهاب الى @Zedthonnbot  وإرسال كـود تيرمكـس هنـا لتسجيل جلسـه اضافيـه اخـرى {var} **\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {name}",
                buttons=get_back_button("multiclient"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{name} Berhasil disettings**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("multiclient"),
        )


@callback(data=re.compile(b"strtri"))
async def strtri(event):
    await event.delete()
    pru = event.sender_id
    var = "STRING_3"
    name = "MULTI CLIENT ke 3"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**- قـم بالذهاب الى @Zedthonnbot  وإرسال كـود تيرمكـس هنـا لتسجيل جلسـه اضافيـه اخـرى {var} **\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {name}",
                buttons=get_back_button("multiclient"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{name} Berhasil disettings**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("multiclient"),
        )


@callback(data=re.compile(b"strfor"))
async def strfor(event):
    await event.delete()
    pru = event.sender_id
    var = "STRING_4"
    name = "MULTI CLIENT ke 4"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**- قـم بالذهاب الى @Zedthonnbot  وإرسال كـود تيرمكـس هنـا لتسجيل جلسـه اضافيـه اخـرى {var} **\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {name}",
                buttons=get_back_button("multiclient"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{name} Berhasil disettings**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("multiclient"),
        )


@callback(data=re.compile(b"strfiv"))
async def strfiv(event):
    await event.delete()
    pru = event.sender_id
    var = "STRING_5"
    name = "MULTI CLIENT ke 5"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"**- قـم بالذهاب الى @Zedthonnbot  وإرسال كـود تيرمكـس هنـا لتسجيل جلسـه اضافيـه اخـرى {var} **\n\n- او اضغـط /cancel للإلغـاء."
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                f"Membatalkan Proses Settings VAR {name}",
                buttons=get_back_button("multiclient"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"**{name} Berhasil disettings**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan.",
            buttons=get_back_button("multiclient"),
        )


@callback(data=re.compile(b"pingbot"))
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    pin = f"🏓 البنـك = {ms} microseconds"
    await event.answer(pin, cache_time=0, alert=True)


@callback(data=re.compile(b"uptimebot"))
async def _(event):
    uptime = await get_readable_time((time.time() - StartTime))
    pin = f"⏱ وقت التشغيـل = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


@asst_cmd(pattern="^/start?([\\s]+)?$", func=lambda e: e.is_private)
async def bot_start(event):
    chat = await event.get_chat()
    user = await event.client.get_me()
    if check_is_black_list(chat.id):
        return
    reply_to = await reply_id(event)
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = user.first_name
    my_last = user.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    if chat.id != OWNER_ID:
        customstrmsg = gvarstatus("START_TEXT") or None
        if customstrmsg is not None:
            start_msg = customstrmsg.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            )
        else:
            start_msg = f"**👋 Hai** {mention}**!**\
                        \n\n**Saya adalah {my_first}** \
                        \n**Anda dapat menghubungi [{OWNER}](tg://user?id={OWNER_ID}) dari sini.**\
                        \n**Jangan melakukan spam atau anda akan di Banned**\
                        \n\n**Powered by** [UserBot](https://github.com/Zed-Thon/Zee-Userbot)"
        buttons = [
            (
                Button.url("- مطـور البـوت", f"https://t.me/{GROUP}"),
                Button.url("- قنـاة البـوت", f"https://t.me/{CHANNEL}"),
            )
        ]
    else:
        start_msg = f"**⎆┊مرحبـاً مطـوري  [{OWNER}](tg://user?id={OWNER_ID})**\
            \n**⎆┊استخـدم ازرار التحـكم والمسـاعده بالاسفـل 🕹**"
        buttons = [
            (Button.inline("الفـارات", data="apiset"),),
            (
                Button.inline("اوامـر البـوت", data="pmbot"),
                Button.inline("المشتـركين", data="users"),
            ),
            (
                Button.inline("البنـك", data="pingbot"),
                Button.inline("وقت التشغيـل", data="uptimebot"),
            ),
            (Button.inline("اغـلاق", data="pmclose"),),
        ]
    try:
        await event.client.send_message(
            chat.id,
            start_msg,
            link_preview=False,
            buttons=buttons,
            reply_to=reply_to,
        )
    except Exception as e:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**ERROR:** Saat Pengguna memulai Bot anda.\n`{e}`",
            )

    else:
        await check_bot_started_users(chat, event)


@asst_cmd(pattern="^/ايدي")
async def _(event):
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await tgbot.send_message(
                event.chat_id,
                "**👥 Chat ID:** `{}`\n**🙋‍♂️ From User ID:** `{}`\n**💎 Bot API File ID:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id), bot_api_file_id
                ),
            )
        else:
            await tgbot.send_message(
                event.chat_id,
                "**👥 Chat ID:** `{}`\n**🙋‍♂️ From User ID:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                ),
            )
    else:
        await tgbot.send_message(
            event.chat_id, f"**👥 Chat ID:** `{str(event.chat_id)}`"
        )


@asst_cmd(pattern="^/بنك$")
async def _(event):
    start = datetime.now()
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await tgbot.send_message(event.chat_id, "🏓**Pong!**\n`%sms`" % duration)
