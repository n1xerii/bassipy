import discord
import yt_dlp as youtube_dl
from discord import FFmpegOpusAudio
from discord.ext import commands
import logging

# FFMPEG
ffmpeg = 'ffmpeg'

# CONNECTION
vc_conn = None

# YOUTUBE DOWNLOAD OPTIONS
ydl_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

# BOT
bot = commands.Bot(command_prefix="!", intents=intents)

# LOGGING
logging.basicConfig(level=logging.ERROR, filename="bot_errors.log")
