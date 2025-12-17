import discord
from discord.ext import commands
import logging

### => TOKEN <= ###
my_token = ""   # Input your Discord bot token

### => PLATFORM <= ###
my_platform = ""    # Input Windows or Linux

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

# BOT
bot = commands.Bot(command_prefix="!", intents=intents)

# LOGGING
logging.basicConfig(level=logging.ERROR, filename="bot_errors.log")
