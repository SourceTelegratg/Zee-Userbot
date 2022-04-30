# zed - userbot
# Copyright (c) 2022 Zed-Userbot
# Credits: @ZedThon || https://github.com/Zed-Thon
#
# This file is a part of < https://github.com/Zed-Thon/Zee-Userbot/ >
# t.me/ZedThon & t.me/zzzzl1l

from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from telethon.tl import types
from telethon.utils import get_display_name

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, PLAY_PIC, QUEUE_PIC, call_py
from userbot.core.vcbot import (
    CHAT_TITLE,
    gen_thumb,
    skip_current_song,
    skip_item,
    ytdl,
    ytsearch,
)
from userbot.core.vcbot.queues import QUEUE, add_to_queue, clear_queue, get_queue
from userbot.utils import edit_delete, edit_or_reply, zed_cmd


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


@zed_cmd(pattern="صوت(?:\s|$)([\s\S]*)", group_only=True)
async def vc_play(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    titlegc = chat.title
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        return await edit_or_reply(event, "**- قـم بـ إدخـال اسم المقطـع الصـوتي للبحـث...**")
    elif replied and not replied.audio and not replied.voice or not replied:
        botzed = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن المقطـٓـع الصـٓـوتي... 🎧♥️╰**")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await botzed.edit(
                "**- عـذراً .. لا يمكن العثور على طلبـك؟!** حاول البحث بعنوان أكثر تحديدًا"
            )
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            titlegc = chat.title
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await botzed.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                caption = f"💡 **تم إضافة المقطـع الصـوتي إلى قائمـة التشغيـل »** `#{pos}`\n\n**🏷 البحـث:** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n🎧 **المستخـدم :** {from_user}"
                await botzed.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            ytlink,
                            HighQualityAudio(),
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                    caption = f"🏷 **البحـث :** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n💡 **التشغـيل:** `جـاري التشغيـل`\n🎧 **المستخـدم :** {from_user}"
                    await botzed.delete()
                    await event.client.send_file(
                        chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await botzed.edit(
                        "**- خطـأ :** `الحساب ليس في الدردشة الصوتية`\n\n• يرجى محاولة التشغيل مرة أخرى"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await botzed.edit(f"`{ep}`")

    else:
        botzed = await edit_or_reply(event, "📥 **- جاري التحميل...**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            songname = "Telegram Music Player"
        elif replied.voice:
            songname = "Voice Note"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            caption = f"💡 **تم إضافة المقطـع الصـوتي إلى قائمـة التشغيـل »** `#{pos}`\n\n**🏷 البحـث:** [{songname}]({link})\n**👥 ايدي الدردشـه:** `{chat_id}`\n🎧 **المستخـدم :** {from_user}"
            await event.client.send_file(
                chat_id, QUEUE_PIC, caption=caption, reply_to=event.reply_to_msg_id
            )
            await botzed.delete()
        else:
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                        HighQualityAudio(),
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                caption = f"🏷 **البحـث :** [{songname}]({link})\n**👥 ايدي الدردشـه:** `{chat_id}`\n💡 **التشغـيل:** `جـاري التشغيـل ✓`\n🎧 **المستخـدم :** {from_user}"
                await event.client.send_file(
                    chat_id, PLAY_PIC, caption=caption, reply_to=event.reply_to_msg_id
                )
                await botzed.delete()
            except AlreadyJoinedError:
                await call_py.leave_group_call(chat_id)
                clear_queue(chat_id)
                await botzed.edit(
                    "**- خطـأ :** `الحساب ليس في الدردشة الصوتية`\n\n• يرجى محاولة التشغيل مرة أخرى"
                )
            except Exception as ep:
                clear_queue(chat_id)
                await botzed.edit(f"`{ep}`")


@zed_cmd(pattern="فيد(?:\s|$)([\s\S]*)", group_only=True)
async def vc_vplay(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    titlegc = chat.title
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.video
        and not replied.document
        and not title
        or not replied
        and not title
    ):
        return await edit_or_reply(event, "**- قـم بـ إدخـال اسم مقطع الفيديـو للبحـث...**")
    if replied and not replied.video and not replied.document:
        xnxx = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن مقطـٓـع الفيـٓـديو... 🎧♥️╰**")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit(
                "**Tidak Dapat Menemukan Video** Coba cari dengan Judul yang Lebih Spesifik"
            )
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"💡 **تم إضافة الفيديو إلى قائمة التشغيل »** `#{pos}`\n\n**🏷 البحـث:** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n🎧 **المستخـدم :** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            hmmm,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await xnxx.edit(
                        f"**🏷 البحـث:** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n💡 **التشغـيل:** `جـاري تشغيل الفيديـو`\n🎧 **المستخـدم :** {from_user}",
                        link_preview=False,
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await xnxx.edit(
                        "**- خطـأ :** `الحساب ليس في الدردشة الصوتية`\n\n• يرجى محاولة التشغيل مرة أخرى"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")

    elif replied:
        xnxx = await edit_or_reply(event, "📥 **- جاري التحميل...**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if len(event.text.split()) < 2:
            RESOLUSI = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            RESOLUSI = int(pq)
        if replied.video or replied.document:
            songname = "Telegram Video Player"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
            caption = f"💡 **تم إضافة الفيديو إلى قائمة التشغيل »** `#{pos}`\n\n**🏷 البحـث:** [{songname}]({link})\n**👥 ايدي الدردشـه:** `{chat_id}`\n🎧 **المستخـدم :** {from_user}"
            await event.client.send_file(
                chat_id, QUEUE_PIC, caption=caption, reply_to=event.reply_to_msg_id
            )
            await xnxx.delete()
        else:
            if RESOLUSI == 360:
                hmmm = LowQualityVideo()
            elif RESOLUSI == 480:
                hmmm = MediumQualityVideo()
            elif RESOLUSI == 720:
                hmmm = HighQualityVideo()
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        hmmm,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
                caption = f"🏷 **البحـث :** [{songname}]({link})\n**👥 ايدي الدردشـه:** `{chat_id}`\n💡 **التشغـيل:** `جـاري تشغيل الفيديـو`\n🎧 **المستخـدم :** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, PLAY_PIC, caption=caption, reply_to=event.reply_to_msg_id
                )
            except AlreadyJoinedError:
                await call_py.leave_group_call(chat_id)
                clear_queue(chat_id)
                await xnxx.edit(
                    "**- خطـأ :** `الحساب ليس في الدردشة الصوتية`\n\n• يرجى محاولة التشغيل مرة أخرى"
                )
            except Exception as ep:
                clear_queue(chat_id)
                await xnxx.edit(f"`{ep}`")
    else:
        xnxx = await edit_or_reply(event, "**- جـاري البحـث ...**")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit("**Tidak Menemukan Video untuk Keyword yang Diberikan**")
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"💡 **تم إضافة الفيديو إلى قائمة التشغيل »** `#{pos}`\n\n🏷 **البحـث :** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n🎧 **المستخـدم :** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            hmmm,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    caption = f"🏷 **البحـث :** [{songname}]({url})\n**⏱ المـدة:** `{duration}`\n💡 **التشغـيل:** `جـاري تشغيل الفيديـو`\n🎧 **المستخـدم :** {from_user}"
                    await xnxx.delete()
                    await event.client.send_file(
                        chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await xnxx.edit(
                        "**- خطـأ :** `الحساب ليس في الدردشة الصوتية`\n\n• يرجى محاولة التشغيل مرة أخرى"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")


@zed_cmd(pattern="انهاء$", group_only=True)
async def vc_end(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await edit_or_reply(event, "**- جـاري الانهـاء...**")
        except Exception as e:
            await edit_delete(event, f"**- خطـأ :** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@zed_cmd(pattern="تخطي(?:\s|$)([\s\S]*)", group_only=True)
async def vc_skip(event):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await edit_delete(event, "**Tidak Sedang Memutar Streaming**")
        elif op == 1:
            await edit_delete(event, "antrian kosong, meninggalkan obrolan suara", 10)
        else:
            await edit_or_reply(
                event,
                f"**⏭ Melewati Lagu**\n**🎧 Sekarang Memutar** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Menghapus Lagu Berikut Dari Antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.edit(DELQUE)


@zed_cmd(pattern="تمهل$", group_only=True)
async def vc_pause(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dijeda**")
        except Exception as e:
            await edit_delete(event, f"**- خطـأ :** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@zed_cmd(pattern="تابع$", group_only=True)
async def vc_resume(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dilanjutkan**")
        except Exception as e:
            await edit_or_reply(event, f"**- خطـأ :** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@zed_cmd(pattern=r"الصوت(?: |$)(.*)", group_only=True)
async def vc_volume(event):
    query = event.pattern_match.group(1)
    me = await event.client.get_me()
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    chat_id = event.chat_id
    if not admin and not creator:
        return await edit_delete(event, f"**Maaf {me.first_name} Bukan Admin 👮**", 30)

    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(query))
            await edit_or_reply(
                event, f"**Berhasil Mengubah Volume Menjadi** `{query}%`"
            )
        except Exception as e:
            await edit_delete(event, f"**- خطـأ :** `{e}`", 30)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@zed_cmd(pattern="التشغيل$", group_only=True)
async def vc_playlist(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await edit_or_reply(
                event,
                f"**🎧 جـاري تشغيـل :**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            PLAYLIST = f"**🎧 جـاري تشغيـل :**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3]}` \n\n**• Daftar Putar:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await edit_or_reply(event, PLAYLIST, link_preview=False)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat_id = u.chat_id
    print(chat_id)
    await skip_current_song(chat_id)


@call_py.on_closed_voice_chat()
async def closedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_left()
async def leftvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_kicked()
async def kickedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


CMD_HELP.update(
    {
        "vcplugin": f"**Plugin : **`vcplugin`\
        \n\n  •  **Syntax :** `{cmd}play` <Judul Lagu/Link YT>\
        \n  •  **Function : **Untuk Memutar Lagu di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `{cmd}vplay` <Judul Video/Link YT>\
        \n  •  **Function : **Untuk Memutar Video di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `{cmd}end`\
        \n  •  **Function : **Untuk Memberhentikan video/lagu yang sedang putar di voice chat group\
        \n\n  •  **Syntax :** `{cmd}skip`\
        \n  •  **Function : **Untuk Melewati video/lagu yang sedang di putar\
        \n\n  •  **Syntax :** `{cmd}pause`\
        \n  •  **Function : **Untuk memberhentikan video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `{cmd}resume`\
        \n  •  **Function : **Untuk melanjutkan pemutaran video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `{cmd}volume` 1-200\
        \n  •  **Function : **Untuk mengubah volume (Membutuhkan Hak admin)\
        \n\n  •  **Syntax :** `{cmd}playlist`\
        \n  •  **Function : **Untuk menampilkan daftar putar Lagu/Video\
    "
    }
)
