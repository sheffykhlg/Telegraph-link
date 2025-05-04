from datetime import datetime
from pytz import timezone
from pyrogram import Client, filters
import os, time, re, math
from catbox import CatboxUploader
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, PeerIdInvalid

FORCE_CHANNEL = "ssbotz"

async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ("member", "administrator", "creator")
    except UserNotParticipant:
        return False
    except PeerIdInvalid:
        return False
    except Exception:
        return False

RKN_PROGRESS = """<b>
╭━━━━❰ ʀᴋɴ ᴏᴘᴇʀᴀᴛɪᴏɴ ꜱᴛᴀʀᴛᴇᴅ! ❱━➣
┣⪼ 🗃️ ꜱɪᴢᴇ ʙᴀᴛᴀᴜ: {1} | {2}
┣⪼ ⏳ ᴋᴀᴀᴍ ᴄʜᴀʟ ʀʜᴀ ʜᴀɪ : {0}%
┣⪼ 🚀 ꜱᴘᴇᴇᴅ ɪꜱ ғʟʏɪɴɢ: {3}/s
┣⪼ ⏰ ʜᴏ ᴊᴀʏᴇɢᴀ ɪɴ: {4}
┣⪼ 🤖 ᴅᴇᴠᴛᴀ - @Sheffyssamra
┣⪼ 🛠️ ᴛᴇᴄʜɴɪᴄᴀʟ ᴋᴀᴀʀɪɢᴀʀ - @Sheffyssamra
╰━━━━━━━❰ ᴛʜᴏᴅᴀ ʀᴜᴋ ᴊᴀ ʙʀᴏ... ❱━━━━━➣ </b>"""

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") +         ((str(hours) + "ʜ, ") if hours else "") +         ((str(minutes) + "ᴍ, ") if minutes else "") +         ((str(seconds) + "ꜱ, ") if seconds else "") +         ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2]

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        progress = "{0}{1}".format(
            ''.join(["▣" for i in range(math.floor(percentage / 5))]),
            ''.join(["▢" for i in range(20 - math.floor(percentage / 5))])
        )
        tmp = progress + RKN_PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(text=f"{ud_type}

{tmp}")
        except:
            pass

async def catbox_link_convert(bot, update, edit):
    ext = ""
    if update.photo:
        ext = '.jpg'
    elif update.video:
        ext = '.mp4'
    elif update.document:
        ext = '.mkv'
    elif update.audio:
        ext = '.mp3'
    medianame = "download/" + str(update.from_user.id) + ext
    dl_path = await bot.download_media(message=update, progress=progress_for_pyrogram,
            progress_args=('Uploading to Catbox Server', edit, time.time()), file_name=medianame) if ext else await bot.download_media(message=update, progress=progress_for_pyrogram,
            progress_args=('Uploading to Catbox Server', edit, time.time()))
    uploader = CatboxUploader()
    link = uploader.upload_file(dl_path)
    try:
        os.remove(dl_path)
    except:
        pass
    return link
    

@Client.on_message(filters.command('start') & filters.private)
async def start_command(client, message):
    if not await is_subscribed(client, message.from_user.id):
        try:
            invite_link = await client.export_chat_invite_link(FORCE_CHANNEL)
        except Exception:
            invite_link = f"https://t.me/{FORCE_CHANNEL}"

        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("💠 Join Update Channel 💠", url=invite_link)]
        ])
        return await message.reply_text(
            "**🚫 First join the update channel to use me!**",
            reply_markup=button
        )
    button = InlineKeyboardMarkup([[
    InlineKeyboardButton('🌹 Cʜᴀʟ ʙʜᴀɪ - Uᴘᴅᴀᴛᴇ ᴅᴇᴋʜ!', url='https://t.me/+3MvIV0RlI5A2NTY1'),
    InlineKeyboardButton('☺️ Aʙᴇ ʜᴇʟᴘ ᴄʜᴀʜɪᴇ? Sᴜᴘᴘᴏʀᴛ ʏᴀʀ!', url='https://t.me/Neha_crown_bot')
],[
    InlineKeyboardButton('🎛️ Kᴏɴ ʜᴜ ʙʜᴀɪ - Aʙᴏᴜᴛ ᴘᴀᴅʜ ʟᴇ', callback_data='about'),
    InlineKeyboardButton('🛠️ ᴋʏᴀ ᴄʜᴀʜɪᴇ ʙᴏʟ - Hᴇʟᴘ ʟᴇ ʙʀᴏ', callback_data='help')
],[
    InlineKeyboardButton('💯 Jᴏɪɴ ᴋᴀʀ ʀᴇ - Uᴘᴅᴀᴛᴇs Wᴀʟɪ Fᴀᴍ', url="https://t.me/ssbotz")
]])
    await message.reply_text("ʜᴇʏ ɪ ᴍ ᴛᴇʟᴇɢʀᴀᴘʜ ʙᴏᴛ\nɪ ᴍ ᴀɴʏ ᴠᴇᴅɪᴏ, ɪᴍɢ , ᴍᴘ𝟹, ɢɪғ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ʟɪɴᴋ\nsʜᴀʀᴇ ᴡɪᴛʜ ᴜ ʀ ғʀɪᴇɴᴅs 😄\n\nᴍʏ ᴏᴡɴᴇʀ - @Sheffyssamra\n\nᴍʏ ᴍᴀɪɴᴛᴀɪɴᴇʀ - @Sheffyssamra.", reply_markup=button)

async def file_size_function(update):
    try:
        file = getattr(update, update.media.value)
        if file.file_size > 200 * 1024 * 1024:
            return True
    except:
        return False
        
    return False
        
@Client.on_message(filters.media & filters.private)
async def getmedia(bot, update):
    if await file_size_function(update):
        return await update.reply_text("🥴sᴏʀʀʏ ᴅᴜᴅᴇ, ᴛʜɪs ʙᴏᴛ ᴅᴏᴇsɴ'ᴛ sᴜᴘᴘᴏʀᴛ ғɪʟᴇs ʟᴀʀɢᴇʀ ᴛʜᴀɴ 200 ᴍʙ+😑")
       
    message = await update.reply_text(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
    link = await catbox_link_convert(bot, update, message)
    reply_markup=InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="🌞Open Link💞", url=f"{link}"),
        InlineKeyboardButton(text="🖇️Share Link🙏", url=f"https://telegram.me/share/url?url={link}")
        ],[
        InlineKeyboardButton(text="💯Join Updates Channel💝", url="https://t.me/ssbotz")
        ]])   
    await message.edit_text(
        text=f"ᴛʜɪs ɪs ʏᴏᴜʀ ʟɪɴᴋ\n\nᴛʜᴀɴx 🙂 ғᴏʀ ᴜsɪɴɢ ᴍᴇ ɪ ᴋɴᴏᴡ ɪ ᴍ ʙᴇsᴛ ғᴏʀ ᴜ ᴅᴏɴᴛ ғᴏʀɢᴇᴛ ᴛᴏ sʜᴀʀᴇ ᴡɪᴛʜ ғʀɪɴᴇᴅ ᴀɴᴅ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ʟᴏᴠᴇ ᴜ 💝\n\nLink: `{link}`",
        disable_web_page_preview=False,
        reply_markup=reply_markup)
       
