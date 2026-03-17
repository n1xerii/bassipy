import os

import main
import data
import bot_data

@data.bot.command()
async def play(ctx, url: str):

    main.song = main.get_song(url, ctx)

    main.songs.append(main.song)

    if data.vc_conn is None:
        await main.runplay(ctx)

    if data.vc_conn is not None and data.vc_conn.is_connected():
        if data.vc_conn.is_playing():
            return
        else:
            await main.runplay(ctx)
    else:
        await main.runplay(ctx)

@data.bot.command()
async def skip(ctx):

        if data.vc_conn is None:
            await ctx.send("Join a voice channel first!")
            return

        if main.is_searching:
            await ctx.send("Wait for search to end.")
            return

        ### Temporarily disabled for clarity
        #await main.runskip(ctx)

"""
### Temporarily disabled for clarity
@data.bot.command()
async def search(ctx, *, arg):
    
    if main.is_searching:
        await ctx.send("Already searching.")
        return

    await main.runsearch(ctx, arg=arg)
"""

@data.bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(data.bot.latency * 1000)}ms')
    except Exception as e:
        await ctx.send("Unknown error occurred.")
        print(f"--- An error occurred. Error: {e}")
        return

def Main():
    if bot_data.my_platform.lower() == "windows":
        data.ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
    elif bot_data.my_platform.lower() == "linux":
        data.ffmpeg = 'ffmpeg'

    # RUN BOT
    data.bot.run(bot_data.my_token)

if __name__ == "__main__":
    Main()