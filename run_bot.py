import os
import main
import data
import bot_data

@data.bot.command()
async def play(ctx, url: str):
    try:
        if main.is_playing:
            return
            
        await main.runplay(ctx, url)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@data.bot.command()
async def skip(ctx):
    try:
        if not main.is_playing:
            return

        await main.runskip(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@data.bot.command()
async def search(ctx, *, arg):
    try:
        if main.is_playing or main.is_searching:
            return
        
        await main.runsearch(ctx, arg=arg)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@data.bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(data.bot.latency * 1000)}ms')
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

def Main():
    if (bot_data.my_platform == "windows"):
        data.ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
    elif (bot_data.my_platform == "linux"):
        data.ffmpeg = 'ffmpeg'

    # RUN BOT
    data.bot.run(bot_data.my_token)

if __name__ == "__main__":
    Main()
