import discord
import os
import yt_dlp

print("✅ Step 0: Imports loaded.")

TOKEN = 'MTM3NjU5Mzc2MjgxNzQwOTE1NA.G55xWa.JztK3sglTIUVZTOjCGw5R_kHIe2Quh3EblFPKM'  # 🔐 Replace with actual token

intents = discord.Intents.default()
intents.message_content = True  # ✅ Required for v2.5.2
print("✅ Step 1: Intents set.")

client = discord.Client(intents=intents)
print("✅ Step 2: Discord client created.")

@client.event
async def on_ready():
    print(f"✅ Step 3: {client.user} is now online!")

@client.event
async def on_message(message):
    print(f"📥 Message received: {message.content}")
    
    if message.author == client.user:
        print("ℹ️ Ignored own message.")
        return

    if message.content.startswith('!shorts'):
        print("🔍 Processing !shorts command...")
        parts = message.content.split()
        
        if len(parts) < 2:
            await message.channel.send("❌ Please provide a YouTube Shorts link.")
            print("⚠️ No link provided.")
            return

        url = parts[1]
        await message.channel.send("⏳ Downloading...")
        print(f"⬇️ Downloading from URL: {url}")

        try:
            output_path = "downloads/%(title)s.%(ext)s"
            os.makedirs("downloads", exist_ok=True)
            print("📁 Download folder ready.")

            ydl_opts = {
                'format': 'mp4',
                'outtmpl': output_path,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"✅ Download complete: {filename}")

            await message.channel.send(file=discord.File(filename))
            print("📤 File sent to Discord.")

        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            await message.channel.send(f"⚠️ Error: {e}")

print("🚀 Step 4: Running bot...")
try:
    client.run(TOKEN)
except Exception as e:
    print("❌ Step 5: Failed to start bot")
    print(f"Error: {e}")
