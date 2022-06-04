from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

bot = Client(
    "LOCAL",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await client.send_message(message.chat.id, "Hello there")


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'
    
async def download_progress(current: number, total: number, download_message: Message, file_name: string, started_time: float):
    now = time.time()
    diff = now - started_time
    display_message = None

    if round(diff % 5.00) == 0 or current != total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round(
            (total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        try:
            current_message = """**Download Status**\n\nFile Name: {}\n\nFile Size: {}\n\nDownloaded: {}\n\nETA: {}""".format(
                            file_name,
                            humanbytes(total),
                            humanbytes(current),
                            TimeFormatter(estimated_total_time)
                        )
            if current_message != display_message:
                await download_message.edit_text(
                    text=current_message
                )
                display_message = current_message
        except Exception as e:
            print(str(e))

async def deleteMessage(client: Client, message: Message):
    await client.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id])

@bot.on_message(filters.private and filters.forwarded and filters.video)
async def forwarded_video(client: Client, message: Message):
    # reply_markup_keyboard = [
    #     [
    #     InlineKeyboardButton("📁 File", callback_data='file'),
    #     InlineKeyboardButton("📹 Video", callback_data='video')
    #     ]
    # ]
    # reply_markup = InlineKeyboardMarkup(inline_keyboard=reply_markup_keyboard)
    # await client.send_message(chat_id=message.chat.id, text="Please choose from below!", reply_markup=reply_markup, reply_to_message_id=message.message_id)
    try:
        file_name = message.caption + '.mp4'
    except:
        file_name = 'Video.mp4'
    started_time = time.time()
    download_message = await client.send_message(chat_id=message.chat.id, text="Starting to Download")
    await client.download_media(message, file_name=file_name, progress=download_progress, progress_args=(download_message, file_name, started_time))

print("PingAll is alive!")  
bot.run()