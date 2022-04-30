# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @ZedThon
# FROM Zee-Userbot <https://github.com/Zed-Thon/Zee-Userbot>
# t.me/ZedThon & t.me/zzzzl1l

from asyncio import sleep

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
    UserIdInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS, WHITELIST
from userbot.events import register
from userbot.utils import (
    _format,
    edit_delete,
    edit_or_reply,
    get_user_from_event,
    zed_cmd,
    zed_handler,
    media_type,
)
from userbot.utils.logger import logging

# =================== CONSTANT ===================
PP_TOO_SMOL = "**❈╎الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**❈╎فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "⪼ **أنا لست مشرف هنا!!** 𓆰."
NO_PERM = "⪼ **ليس لدي أذونات كافية!** 𓆰."
NO_SQL = "**Berjalan Pada Mode Non-SQL**"
CHAT_PP_CHANGED = "**❈╎تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔ ╎ ملحق غير صالح  📳** ."

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@zed_cmd(pattern="setgpic( -s| -d)$", group_only=True)
@register(pattern=r"^\.csetgpic( -s| -d)$", sudo=True)
async def set_group_photo(event):
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**- خطـأ : **`{str(e)}`")
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**- خطـأ : **`{e}`")
        await edit_delete(event, "**❈╎تغيّرت صورة الدردشة  🌅**", 30)


@zed_cmd(pattern="رفع مشرف(?:\s|$)([\s\S]*)", group_only=True)
@register(pattern=r"^\.رفع مشرف(?:\s|$)([\s\S]*)", sudo=True)
async def promote(event):
    new_rights = ChatAdminRights(
        add_admins=False,
        change_info=True,
        invite_users=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    eventzed = await edit_or_reply(event, "**╮ ❐.. جـاري ࢪفـع الشخـص ..❏╰**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await eventzed.edit(NO_PERM)
    await edit_delete(eventzed, "**- تم رفـع الشخص مشـرف .. بنجـاح ✓**", 30)


@zed_cmd(pattern="تنزيل مشرف(?:\s|$)([\s\S]*)", group_only=True)
@register(pattern=r"^\.تنزيل مشرف(?:\s|$)([\s\S]*)", sudo=True)
async def demote(event):
    "To demote a person in group"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    eventzed = await edit_or_reply(event, "**╮ ❐.. جـاري تنزيـل الشخـص ..❏╰**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
        manage_call=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await eventzed.edit(NO_PERM)
    await edit_delete(eventzed, "**- تم تنزيـل الشخـص مشرف .. بنجـاح✓**", 30)


@zed_cmd(pattern="حظر(?:\s|$)([\s\S]*)", group_only=True)
@register(pattern=r"^\.حظر(?:\s|$)([\s\S]*)", sudo=True)
async def ban(bon):
    me = await bon.client.get_me()
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_or_reply(bon, NO_ADMIN)

    user, reason = await get_user_from_event(bon)
    if not user:
        return
    zed = await edit_or_reply(bon, "**╮ ❐... جـاࢪِ الحـظـࢪ ...❏╰**")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await edit_or_reply(bon, NO_PERM)
    if - الـسبب :
        await zed.edit(
            r"\\**#الحظـر**//"
            f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
            f"**- الايـدي :** `{str(user.id)}`\n"
            f"**- الـسبب :** `{reason}`",
        )
    else:
        await zed.edit(
            f"\\\\**#الحظـر**//\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n**- الايـدي :** `{user.id}`\n**- الكـاتم :** `تم حظـره بواسطـة {me.first_name}`",
        )


@zed_cmd(pattern="الغاء حظر(?:\s|$)([\s\S]*)", group_only=True)
@register(pattern=r"^\.الغاء حظر(?:\s|$)([\s\S]*)", sudo=True)
async def nothanos(unbon):
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_delete(unbon, NO_ADMIN)
    zed = await edit_or_reply(unbon, "**╮ ❐.. جـاري الغاء حـظࢪه ..❏╰**")
    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await edit_delete(zed, "** - تم الغـاء الحظـر .. بنجـاح✓**")
    except UserIdInvalidError:
        await edit_delete(zed, "`Sepertinya Terjadi ERROR!`")


@zed_cmd(pattern="كتم(?: |$)(.*)", group_only=True)
@register(pattern=r"^\.كتم(?: |$)(.*)", sudo=True)
async def spider(spdr):
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await edit_or_reply(spdr, NO_SQL)
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_or_reply(spdr, NO_ADMIN)
    zed = await edit_or_reply(spdr, "**╮ ❐ ... جـاࢪِ الکتم ... ❏╰**")
    user, reason = await get_user_from_event(spdr)
    if not user:
        return
    self_user = await spdr.client.get_me()
    if user.id == self_user.id:
        return await edit_or_reply(zed, "**Tidak Bisa Membisukan Diri Sendiri..（>﹏<）**")
    if user.id in DEVS:
        return await zed.edit("**Gagal Mute, dia adalah Pembuat Saya 🤪**")
    if user.id in WHITELIST:
        return await zed.edit("**Gagal Mute, dia adalah admin @SharingUserbot 🤪**")
    await zed.edit(
        r"\\**#الكـتم**//"
        f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
        f"**- الايـدي :** `{user.id}`\n"
        f"**- الكـاتم :** `تم كتمـه بواسطـة {self_user.first_name}`",
    )
    if mute(spdr.chat_id, user.id) is False:
        return await edit_delete(zed, "**ERROR:** `Pengguna Sudah Dibisukan.`")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
        if - الـسبب :
            await zed.edit(
                r"\\**#الكـتم**//"
                f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**- الايـدي :** `{user.id}`\n"
                f"**- الـسبب :** `{reason}`",
            )
        else:
            await zed.edit(
                r"\\**#الكـتم**//"
                f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**- الايـدي :** `{user.id}`\n"
                f"**- الكـاتم :** `تم كتمـه بواسطـة {self_user.first_name}`",
            )
    except UserIdInvalidError:
        return await edit_delete(zed, "**Terjadi ERROR!**")


@zed_cmd(pattern="الغاء كتم(?: |$)(.*)", group_only=True)
@register(pattern=r"^\.الغاء كتم(?: |$)(.*)", sudo=True)
async def unmoot(unmot):
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_delete(unmot, NO_ADMIN)
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)
    zed = await edit_or_reply(unmot, "**╮ ❐ ... جـاࢪِ الغـاء الکتم ... ❏╰**")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await edit_delete(unmot, "**ERROR! Pengguna Sudah Tidak Dibisukan.**")
    try:
        await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
        await edit_delete(zed, "**Berhasil Melakukan Unmute!**")
    except UserIdInvalidError:
        return await edit_delete(zed, "**Terjadi ERROR!**")


@zed_handler(incoming=True)
async def muter(moot):
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                )
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@zed_cmd(pattern="الغاء الكتم العام(?: |$)(.*)")
@register(pattern=r"^\.الغاء الكتم العام(?: |$)(.*)", sudo=True)
async def ungmoot(un_gmute):
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_delete(un_gmute, NO_ADMIN)
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        return await edit_delete(un_gmute, NO_SQL)
    zed = await edit_or_reply(un_gmute, "**╮ ❐ ... جـاࢪِ الغـاء الکتم العـام ... ❏╰**")
    user = await get_user_from_event(un_gmute)
    user = user[0]
    if not user:
        return
    await zed.edit("`Membuka Global Mute Pengguna...`")
    if ungmute(user.id) is False:
        await zed.edit("**ERROR!** Pengguna Sedang Tidak Di Gmute.")
    else:
        await edit_delete(un_gmute, "**Berhasil! Pengguna Sudah Tidak Dibisukan**")


@zed_cmd(pattern="كتم عام(?: |$)(.*)")
@register(pattern=r"^\.كتم عام(?: |$)(.*)", sudo=True)
async def gspider(gspdr):
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_delete(gspdr, NO_ADMIN)
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        return await gspdr.edit(NO_SQL)
    zed = await edit_or_reply(gspdr, "**╮ ❐ ... جـاࢪِ الکتم عـام ... ❏╰**")
    user, reason = await get_user_from_event(gspdr)
    if not user:
        return
    self_user = await gspdr.client.get_me()
    if user.id == self_user.id:
        return await zed.edit("**Tidak Bisa Membisukan Diri Sendiri..（>﹏<）**")
    if user.id in DEVS:
        return await zed.edit("**Gagal Global Mute, Dia Adalah Pembuat Saya 🤪**")
    if user.id in WHITELIST:
        return await zed.edit("**Gagal Mute, dia adalah admin @SharingUserbot 🤪**")
    await zed.edit("**Berhasil Membisukan Pengguna!**")
    if gmute(user.id) is False:
        await edit_delete(gspdr, "**ERROR! Pengguna Sudah Dibisukan.**")
    elif - الـسبب :
        await zed.edit(
            r"\\**#الكـتم_عـام**//"
            f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
            f"**- الايـدي :** `{user.id}`\n"
            f"**- الـسبب :** `{reason}`",
        )
    else:
        await zed.edit(
            r"\\**#الكـتم_عـام**//"
            f"\n\n**- الاسـم :** [{user.first_name}](tg://user?id={user.id})\n"
            f"**- الايـدي :** `{user.id}`\n"
            f"**- الكـاتم :** `تم كتمـه عـام بواسطـة {self_user.first_name}`",
        )


@zed_cmd(pattern="المحذوفين(?: |$)(.*)", group_only=True)
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**Grup Bersih, Tidak Menemukan Akun Terhapus.**"
    if con != "clean":
        await show.edit("`Mencari Akun Depresi...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"**Menemukan** `{del_u}` **Akun Depresi/Terhapus/Zombie Dalam Grup Ini,"
                "\nBersihkan Itu Menggunakan Perintah** `.zombies clean`"
            )
        return await show.edit(del_status)
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await show.edit("**Maaf Kamu Bukan Admin!**")
    await show.edit("`Menghapus Akun Depresi...`")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Tidak Memiliki Izin Banned Dalam Grup Ini`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
    if del_u > 0:
        del_status = f"**Membersihkan** `{del_u}` **Akun Terhapus**"
    if del_a > 0:
        del_status = (
            f"**Membersihkan** `{del_u}` **Akun Terhapus** "
            f"\n`{del_a}` **Akun Admin Yang Terhapus Tidak Dihapus.**"
        )
    await show.edit(del_status)
    await sleep(2)
    await show.delete()
    if BOTLOG_CHATID:
        await show.client.send_message(
            BOTLOG_CHATID,
            "**#ZOMBIES**\n"
            f"**Membersihkan** `{del_u}` **Akun Terhapus!**"
            f"\n**GRUP:** {show.chat.title}(`{show.chat_id}`)",
        )


@zed_cmd(pattern="المشرفون$", group_only=True)
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "Grup Ini"
    mentions = f"<b>👑 قائمـة مشـرفين كـروب {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n⚜️ {link}"
            else:
                mentions += f"\n⚜ Akun Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += f" {str(err)}" + "\n"
    await show.edit(mentions, parse_mode="html")


@zed_cmd(pattern="تثبيت( loud|$)", group_only=True)
@register(pattern=r"^\.تثبيت( loud|$)", sudo=True)
async def pin(event):
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**- بالـرد ع رسـاله .. للتثبيت**", 30)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "**- تم تثبيت الرسـاله .. بنجـاح✓**")


@zed_cmd(pattern="الغاء تثبيت( all|$)", group_only=True)
@register(pattern=r"^\.الغاء تثبيت( all|$)", sudo=True)
async def unpin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "**Reply ke Pesan untuk melepas Pin atau Gunakan** `.unpin all` **untuk melepas pin semua**",
            45,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event,
                "**Reply ke Pesan untuk melepas pin atau gunakan** `.unpin all`",
                45,
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "**- تم الغـاء تثبيت الرسالـه بنجـاح✓**")


@zed_cmd(pattern="طرد(?: |$)(.*)", group_only=True)
@register(pattern=r"^\.طرد(?: |$)(.*)", sudo=True)
async def kick(usr):
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await edit_delete(usr, NO_ADMIN)
    user, reason = await get_user_from_event(usr)
    if not user:
        return await edit_delete(usr, "**Tidak Dapat Menemukan Pengguna.**")
    xxnx = await edit_or_reply(usr, "**╮ ❐.. جـاري الطـࢪد ..❏╰**")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await edit_delete(usr, f"{NO_PERM}\n{e}")
    if - الـسبب :
        await xxnx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**\n**Alasan:** `{reason}`"
        )
    else:
        await xxnx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**",
        )


@zed_cmd(pattern=r"undlt( -u)?(?: |$)(\d*)?", group_only=True)
async def _iundlt(event):
    catevent = await edit_or_reply(event, "`Searching recent actions...`")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**{lim} Pesan yang dihapus di grup ini:**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )


CMD_HELP.update(
    {
        "admin": f"**Plugin : **`admin`\
        \n\n  •  **Syntax :** `{cmd}promote <username/reply> <nama title (optional)>`\
        \n  •  **Function : **Mempromosikan member sebagai admin.\
        \n\n  •  **Syntax :** `{cmd}demote <username/balas ke pesan>`\
        \n  •  **Function : **Menurunkan admin sebagai member.\
        \n\n  •  **Syntax :** `{cmd}ban <username/balas ke pesan> <alasan (optional)>`\
        \n  •  **Function : **Membanned Pengguna dari grup.\
        \n\n  •  **Syntax :** `{cmd}unban <username/reply>`\
        \n  •  **Function : **Unbanned pengguna jadi bisa join grup lagi.\
        \n\n  •  **Syntax :** `{cmd}mute <username/reply> <alasan (optional)>`\
        \n  •  **Function : **Membisukan Seseorang Di Grup, Bisa Ke Admin Juga.\
        \n\n  •  **Syntax :** `{cmd}unmute <username/reply>`\
        \n  •  **Function : **Membuka bisu orang yang dibisukan.\
        \n  •  **Function : ** Membuka global mute orang yang dibisukan.\
        \n\n  •  **Syntax :** `{cmd}all`\
        \n  •  **Function : **Tag semua member dalam grup.\
        \n\n  •  **Syntax :** `{cmd}admins`\
        \n  •  **Function : **Melihat daftar admin di grup.\
        \n\n  •  **Syntax :** `{cmd}setgpic <flags> <balas ke gambar>`\
        \n  •  **Function : **Untuk mengubah foto profil grup atau menghapus gambar foto profil grup.\
        \n  •  **Flags :** `-s` = **Untuk mengubah foto grup** atau `-d` = **Untuk menghapus foto grup**\
    "
    }
)


CMD_HELP.update(
    {
        "pin": f"**Plugin : **`pin`\
        \n\n  •  **Syntax :** `{cmd}pin` <reply chat>\
        \n  •  **Function : **Untuk menyematkan pesan dalam grup.\
        \n\n  •  **Syntax :** `{cmd}pin loud` <reply chat>\
        \n  •  **Function : **Untuk menyematkan pesan dalam grup (tanpa notifikasi) / menyematkan secara diam diam.\
        \n\n  •  **Syntax :** `{cmd}unpin` <reply chat>\
        \n  •  **Function : **Untuk melepaskan pin pesan dalam grup.\
        \n\n  •  **Syntax :** `{cmd}unpin all`\
        \n  •  **Function : **Untuk melepaskan semua sematan pesan dalam grup.\
    "
    }
)


CMD_HELP.update(
    {
        "undelete": f"**Plugin : **`undelete`\
        \n\n  •  **Syntax :** `{cmd}undlt` <jumlah chat>\
        \n  •  **Function : **Untuk mendapatkan pesan yang dihapus baru-baru ini di grup\
        \n\n  •  **Syntax :** `{cmd}undlt -u` <jumlah chat>\
        \n  •  **Function : **Untuk mendapatkan pesan media yang dihapus baru-baru ini di grup \
        \n  •  **Flags :** `-u` = **Gunakan flags ini untuk mengunggah media.**\
        \n\n  •  **NOTE : Membutuhkan Hak admin Grup** \
    "
    }
)


CMD_HELP.update(
    {
        "gmute": f"**Plugin : **`gmute`\
        \n\n  •  **Syntax :** `{cmd}gmute` <username/reply> <alasan (optional)>\
        \n  •  **Function : **Untuk Membisukan Pengguna di semua grup yang kamu admin.\
        \n\n  •  **Syntax :** `{cmd}ungmute` <username/reply>\
        \n  •  **Function : **Untuk Membuka global mute Pengguna di semua grup yang kamu admin.\
    "
    }
)


CMD_HELP.update(
    {
        "zombies": f"**Plugin : **`zombies`\
        \n\n  •  **Syntax :** `{cmd}zombies`\
        \n  •  **Function : **Untuk mencari akun terhapus dalam grup\
        \n\n  •  **Syntax :** `{cmd}zombies clean`\
        \n  •  **Function : **untuk menghapus Akun Terhapus dari grup.\
    "
    }
)
