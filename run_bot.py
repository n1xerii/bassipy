import os

import main
import data
import bot_data

@data.bot.command()
async def play(ctx, url: str):

    # If user is not in a voice channel, prompt to join one
    if not ctx.author.voice:
        main.songs.clear()
        await ctx.send("Join a voice channel first!")
        return

    main.song = main.get_song(url, ctx)
    main.songs.append(main.song)

    if len(main.songs) == 1:
        await ctx.send("Playing started!")
    else:
        await ctx.send("Song added to queue!")

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

        #if data.vc_conn is None:
        #    await ctx.send("Join a voice channel first!")
        #    return

        if main.is_searching:
            await ctx.send("Wait for search to end.")
            return

        await main.runskip(ctx)

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
    else:
        print("--- No platform provided.")
        return

    # RUN BOT
    if bot_data.my_token is None or bot_data.my_token == "":
        print("--- No token provided.")
        return
    else:
        data.bot.run(bot_data.my_token)

if __name__ == "__main__":
    Main()
