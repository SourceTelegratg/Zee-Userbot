""" Userbot module for other small commands. """
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, zed_cmd


@zed_cmd(pattern="ihelp$")
async def usit(event):
    me = await event.client.get_me()
    await edit_or_reply(
        event,
        f"**Hai {me.first_name} Kalo Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.help` Atau Bisa Minta Bantuan Ke:\n"
        f"✣ **Group Support :** [ZThon Support](t.me/ZedThon_Group)\n"
        f"✣ **Channel Zee :** [Zea Store](t.me/ZedThon)\n"
        f"✣ **Owner Repo :** [زلــزال الهيبــه](t.me/zzzzl1l)\n"
        f"✣ **Repo :** [Zee-Userbot](https://github.com/Zed-Thon/Zee-Userbot)\n",
    )


@zed_cmd(pattern="الفارات$")
async def var(event):
    await edit_or_reply(
        event,
        "**Daftar Lengkap Vars Dari Zee-Userbot:** [KLIK DISINI](https://telegra.ph/List-Variabel-Heroku-untuk-Zed-Userbot-09-22)",
    )


CMD_HELP.update(
    {
        "helper": f"**Plugin : **`helper`\
        \n\n  •  **Syntax :** `{cmd}ihelp`\
        \n  •  **Function : **Bantuan Untuk Zee-Userbot.\
        \n\n  •  **Syntax :** `{cmd}listvar`\
        \n  •  **Function : **Melihat Daftar Vars.\
        \n\n  •  **Syntax :** `{cmd}repo`\
        \n  •  **Function : **Melihat Repository Zee-Userbot.\
        \n\n  •  **Syntax :** `{cmd}string`\
        \n  •  **Function : **Link untuk mengambil String Zee-Userbot.\
    "
    }
)
