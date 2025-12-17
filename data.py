import os
import asyncio
import discord
import yt_dlp as youtube_dl
from discord import FFmpegOpusAudio

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
