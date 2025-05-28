import discord
from discord.ext import commands
import os
import yt_dlp
import asyncio
from upload_to_youtube import upload_video

TOKEN = 'MTM3NjU5Mzc2MjgxNzQwOTE1NA.G55xWa.JztK3sglTIUVZTOjCGw5R_kHIe2Quh3EblFPKM'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

queue = asyncio.Queue()

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    bot.loop.create_task(process_queue())

@bot.command(name='shorts')
async def shorts(ctx, url: str = None):
    if url is None:
        await ctx.send("❌ Please provide a YouTube Shorts link.")
        return

    await ctx.send("📥 Added to queue. You'll be notified once your Shorts is uploaded.")
    await queue.put((ctx, url))

async def process_queue():
    while True:
        ctx, url = await queue.get()
        try:
            await process_shorts(ctx, url)
        except Exception as e:
            await ctx.send(f"❌ Unexpected error: {e}")
        queue.task_done()

async def process_shorts(ctx, url):
    await ctx.send("⏳ Processing your Shorts...")

    try:
        os.makedirs("downloads", exist_ok=True)
        output_path = "downloads/%(id)s.%(ext)s"  # Safe filename

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': output_path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get("title", "Untitled")

        await ctx.send("✅ Download complete. Uploading to YouTube...")
        await ctx.send(f"🎞️ Title: **{title}**")

        video_id = upload_video(filename, title)

        await ctx.send(f"🎬 Uploaded to YouTube: https://youtu.be/{video_id}")

        os.remove(filename)
        print(f"🗑️ Deleted local file: {filename}")

    except Exception as e:
        await ctx.send(f"❌ Error while processing: {e}")

bot.run(TOKEN)
