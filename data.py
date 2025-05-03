import os
import asyncio
import discord
import logging
import yt_dlp as youtube_dl
from discord.ext import commands
from discord import FFmpegOpusAudio

# FFMPEG
ffmpeg = 'ffmpeg'

# LOGGING
logging.basicConfig(level=logging.ERROR, filename="bot_errors.log")    # Logging

# CONNECTION
vc_conn = None

# YOUTUBE DOWNLOAD OPTIONS
ydl_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}
