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
    
    # Voice channel of user
    vc_to_join = ctx.author.voice.channel

    # Connect to the channel
    if data.vc_conn is None:
        data.vc_conn = await vc_to_join.connect()
    if not data.vc_conn.is_connected():
        main.songs.clear()
        await vc_to_join.connect()

    # Get song data and add to queue list
    requested_song = main.get_song_data(url, ctx)
    main.add_song_to_queue(requested_song)

    # Check for first song
    #if len(main.songs) == 1 and not data.vc_conn.is_playing():
    #    await ctx.send("Playing started!")

    await ctx.send(f"**| 🎵 QUEUE |**\n")
    for s in main.songs:
        await ctx.send(
            f"- *{s['title']}*\n"
        )

    if data.vc_conn.is_playing():
        return
    await main.song_player(ctx)


@data.bot.command()
async def skip(ctx):
        #if not ctx.author.voice:
        #    await ctx.send("Not in a voice channel.")
        #    return

        if data.vc_conn is None:
            await ctx.send("No voice connection.")
            return

        if main.is_searching:
            await ctx.send("Wait for search to end.")
            return

        await main.song_skipper(ctx)


@data.bot.command()
async def search(ctx, *, arg):
    if data.vc_conn is None:
        vc_to_join = ctx.author.voice.channel
        data.vc_conn = await vc_to_join.connect()

    if main.is_searching:
        await ctx.send("Wait for current search to end.")
        return

    await main.song_searcher(ctx, arg=arg)

@data.bot.command()
async def queue(ctx):
    if not main.songs:
        await ctx.send("Queue is empty.")
        return

    message = "**QUEUE**\n" + "\n".join(
        f"- {s['title']}" for s in main.songs
    )

    await ctx.send(message)



@data.bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(data.bot.latency * 1000)}ms')
    except Exception as e:
        print(f"--- Unknown error occurred: {e}")
        await ctx.send("Unknown error occurred.")
        return


def Main():
    # Set ffmpeg to system-wide ffmpeg
    data.ffmpeg = 'ffmpeg'

    # Start bot
    if bot_data.my_token is None or bot_data.my_token == "":
        print("--- [BASSIPY] : No token provided.")
        return
    data.bot.run(bot_data.my_token)

if __name__ == "__main__":
    Main()
