import os
from bot_instance import bot
from bot_token import my_token, my_platform
import main
import data

@bot.command()
async def play(ctx, url: str):
    try:
        if main.is_playing:
            return
            
        await main.runplay(ctx, url)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@bot.command()
async def skip(ctx):
    try:
        if not main.is_playing:
            return

        await main.runskip(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@bot.command()
async def search(ctx, *, arg):
    try:
        if main.is_playing or main.is_searching:
            return
        
        await main.runsearch(ctx, arg=arg)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(bot.latency * 1000)}ms')
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

def Main():
    if (my_platform == "windows"):
        data.ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
    elif (my_platform == "linux"):
        data.ffmpeg = 'ffmpeg'

    # RUN BOT
    bot.run(my_token)

if __name__ == "__main__":
    Main()
