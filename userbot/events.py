# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for managing events. One of the main components of the userbot."""

import inspect
import re
import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from pathlib import Path
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import CMD_HANDLER, CMD_LIST, DEFAULT, DEVS, ZED2, ZED3, ZED4, ZED5, bot


def zed_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    args.get("allow_sudo", False)
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            if len(CMD_HANDLER) == 2:
                catreg = "^" + CMD_HANDLER
                reg = CMD_HANDLER[1]
            elif len(CMD_HANDLER) == 1:
                catreg = "^\\" + CMD_HANDLER
                reg = CMD_HANDLER
            args["pattern"] = re.compile(catreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})

    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]

    return events.NewMessage(**args)


def command(**args):
    args["func"] = lambda e: e.via_bot_id is None

    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    pattern = args.get("pattern")
    allow_edited_updates = args.get("allow_edited_updates", False)
    args["incoming"] = args.get("incoming", False)
    args["outgoing"] = True
    if bool(args["incoming"]):
        args["outgoing"] = False

    try:
        if pattern is not None and not pattern.startswith("(?i)"):
            args["pattern"] = "(?i)" + pattern
    except BaseException:
        pass

    reg = re.compile("(.*)")
    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                return
            if not trigger_on_fwd and check.fwd_from:
                return

            if groups_only and not check.is_group:
                await check.respond("`I don't think this is a group.`")
                return

        if allow_edited_updates:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))

    return decorator


def register(**args):
    """Register a new event."""
    pattern = args.get("pattern")
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    groups_only = args.get("groups_only", False)
    trigger_on_fwd = args.get("trigger_on_fwd", False)
    disable_errors = args.get("disable_errors", False)
    insecure = args.get("insecure", False)
    args.get("sudo", False)
    args.get("own", False)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "sudo" in args:
        del args["sudo"]
        args["incoming"] = True
        args["from_users"] = DEVS

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "groups_only" in args:
        del args["groups_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "trigger_on_fwd" in args:
        del args["trigger_on_fwd"]

    if "own" in args:
        del args["own"]
        args["incoming"] = True
        args["from_users"] = DEFAULT

    if "insecure" in args:
        del args["insecure"]

    if pattern and not ignore_unsafe:
        args["pattern"] = pattern.replace("^.", unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                # Messages sent in channels can be edited by other users.
                # Ignore edits that take place in channels.
                return
            if not trigger_on_fwd and check.fwd_from:
                return

            if groups_only and not check.is_group:
                await check.respond("- لا اعتقـد ان هـذا كـروب ؟!")
                return

            if check.via_bot_id and not insecure and check.out:
                return

            try:
                await func(check)

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:

                # Check if we have to disable it.
                # If not silence the log spam on the console,
                # with a dumb except.

                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**✘ تقـريـر خطـأ زدثـــون 𝗭𝗧𝗵𝗼𝗻 ✘**\n\n"
                    link = "[𐇮 𝙕𝞝𝙇𝙕𝘼𝙇 الهہـيـٖ͡ـ͢ـبـه 𐇮](https://t.me/zzzzl1l)"
                    text += "- يمكنك الإبـلاغ عن هـذا الخطـأ .. "
                    text += f"فقط قم بإعـادة توجيـه هـذه الرسـالة إلى مطـور السـورس {link}.\n\n"

                    ftext = "========== DISCLAIMER =========="
                    ftext += "\nيتم تحميل هذا الملف فقط هنا ،"
                    ftext += "\nنسجل فقـط تقريـر الخطـأ وتـاريخـه ،"
                    ftext += "\nنحن نحترم خصوصيتك."
                    ftext += "\n- يمكنـك الإبـلاغ عن هـذا الخطـأ .. "
                    ftext += "\nفقـط قـم بإعـادة توجيـه هـذه الرسـالة إلى مطـور السـورس @zzzzl1l"
                    ftext += "\n================================\n\n"
                    ftext += "--------بـدء سجـل تتبـع زدثـــون 𝗭𝗧𝗵𝗼𝗻--------\n"
                    ftext += "\n- التـاريخ : " + date
                    ftext += "\n- ايـدي الكـروب : " + str(check.chat_id)
                    ftext += "\n- ايـدي الشخـص : " + str(check.sender_id)
                    ftext += "\n\n- تقـرير الحـدث :\n"
                    ftext += str(check.text)
                    ftext += "\n\n- تفاصـيل التتبـع :\n"
                    ftext += str(format_exc())
                    ftext += "\n\n- رسـالة الخطـأ:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------نهـاية سجـل تتبـع زدثـــون 𝗭𝗧𝗵𝗼𝗻--------"

                    command = 'git log --pretty=format:"%an: %s" -10'

                    ftext += "\n\n\n- آخـر 10 ملفـات تم تحديثهـا :\n"

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    with open("error.log", "w+") as file:
                        file.write(ftext)

        if bot:
            if not disable_edited:
                bot.add_event_handler(wrapper, events.MessageEdited(**args))
            bot.add_event_handler(wrapper, events.NewMessage(**args))
        if ZED2:
            if not disable_edited:
                ZED2.add_event_handler(wrapper, events.MessageEdited(**args))
            ZED2.add_event_handler(wrapper, events.NewMessage(**args))
        if ZED3:
            if not disable_edited:
                ZED3.add_event_handler(wrapper, events.MessageEdited(**args))
            ZED3.add_event_handler(wrapper, events.NewMessage(**args))
        if ZED4:
            if not disable_edited:
                ZED4.add_event_handler(wrapper, events.MessageEdited(**args))
            ZED4.add_event_handler(wrapper, events.NewMessage(**args))
        if ZED5:
            if not disable_edited:
                ZED5.add_event_handler(wrapper, events.MessageEdited(**args))
            ZED5.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
