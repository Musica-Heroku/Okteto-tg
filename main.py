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

print("PingAll is alive!")  
bot.run()