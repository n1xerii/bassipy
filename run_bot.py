import os

import main
import data
import bot_data

@data.bot.command()
async def play(ctx, url: str):

    # If user is not in a voice channel, prompt to join one
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first!")
        return

    vc_to_join = ctx.author.voice.channel

    # Connect to the voice channel
    if data.vc_conn is None:
        data.vc_conn = await vc_to_join.connect()

    if not data.vc_conn.is_connected():
        main.songs.clear()
        await vc_to_join.connect()

    song = main.get_song_data(url, ctx)
    main.add_song_to_queue(song)

    # Check for first song
    if len(main.songs) == 1 and not data.vc_conn.is_playing():
        await ctx.send("Playing started!")

    if data.vc_conn.is_connected():
        await main.song_player(ctx)
    else:
        print("No connection. Unknown reason.")


@data.bot.command()
async def skip(ctx):
        if not ctx.author.voice:
            await ctx.send("Not in a voice channel.")
            return

        if data.vc_conn is None:
            await ctx.send("No voice connection.")
            return

        if main.is_searching:
            await ctx.send("Wait for search to end.")
            return

        await main.song_skipper(ctx)


@data.bot.command()
async def search(ctx, *, arg):
    
    if main.is_searching:
        await ctx.send("Wait for current search to end.")
        return

    await main.song_searcher(ctx, arg=arg)


@data.bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(data.bot.latency * 1000)}ms')
    except Exception as e:
        await ctx.send("Unknown error occurred.")
        print(f"--- Unknown error occurred: {e}")
        return


def Main():
    # Platform check
    if bot_data.my_platform.lower() == "windows":
        try:
            data.ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
        except Exception as e:
            print(f"--- Unknown error occured: {e}")
    elif bot_data.my_platform.lower() == "linux":
        try:
            data.ffmpeg = 'ffmpeg'
        except Exception as e:
            print(f"--- Error occured: {e}")
            print(f"--- For Linux, use system-wide ffmpeg.")
    else:
        print("--- No platform provided.")
        return

    # Start bot
    if bot_data.my_token is None or bot_data.my_token == "":
        print("--- No token provided.")
        return
    data.bot.run(bot_data.my_token)

if __name__ == "__main__":
    Main()
