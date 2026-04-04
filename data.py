import discord
from discord.ext import commands
import logging

# INTENTS
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.bans = False
intents.auto_moderation = False

# BOT
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, max_ratelimit_timeout=10)

# FFMPEG
ffmpeg = 'ffmpeg'
ffmpeg_options = {
    'before_options': (
        '-reconnect 1 '
        '-reconnect_streamed 1 '
        '-reconnect_delay_max 5'
    )
}

# CONNECTION
vc_conn = None

# YDL OPTIONS
ydl_options = {
    "format": "bestaudio/best", # just "bestaudio" ??
    "noplaylist": True,
    "quiet": True,
    #"extract_flat": False,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

# LOGGING
logging.basicConfig(filename="bot.log")
