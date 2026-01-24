import os
import asyncio
import discord
import logging
import yt_dlp as youtube_dl
from discord.ext import commands
from discord import FFmpegOpusAudio

import data

is_playing = False
is_searching = False

# PLAY COMMAND
# | Plays any audio from Youtube in a Discord Voice Channel
async def runplay(ctx, url: str):
    global is_playing

    try:
        # If user is not present in a voice channel, stop execution
        if not ctx.author.voice:
            await ctx.send("Join a voice channel first!")
            return

        vc_to_join = ctx.author.voice.channel

        # Connect to the voice channel
        data.vc_conn = await vc_to_join.connect()

        # Set is_playing to true to prevent running the play command again during playback
        is_playing = True

        # Prepare file
        with youtube_dl.YoutubeDL(data.ydl_options) as ydl:
            infoDict = ydl.extract_info(url, download=True)
            audioFile = ydl.prepare_filename(infoDict)

        # Check whether file is found before playing, if not, stop execution
        if not os.path.isfile(audioFile):
            ctx.send(f"Audio file not found: {audioFile}")
            return

        # Prepare audio source
        audio_source = FFmpegOpusAudio(audioFile, executable=data.ffmpeg)

        # Play audio source in voice channel
        data.vc_conn.play(audio_source)

        # Keep playing the song until it ends
        while data.vc_conn.is_playing():
            await asyncio.sleep(1)

        # Delete audio file
        os.remove(audioFile)

        # Set is_playing to false to allow running play command again
        is_playing = False

        await data.vc_conn.disconnect()
        await ctx.send("Finished playing audio.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await ctx.send(f"An error occurred: {e}")
        return


# SKIP COMMAND
# | Skips the currently playing video/song if one is playing
async def runskip(ctx):
    global is_playing

    # If audio is playing, skip the current song and disconnect
    if (data.vc_conn is not None):
        data.vc_conn.stop()
        await ctx.send("Song skipped!")
        await data.vc_conn.disconnect()

    is_playing = False


# SEARCH COMMAND
# | Searches 5 top results for "arg" from Youtube and provides 5 buttons to select any of them to play
async def runsearch(ctx, *, arg):
    global is_searching
    
    try:
        await ctx.send("Searching... Please wait...")

        is_searching = True
        
        # Call "ytsearch5" from ytdlp and populate "videos" with the result
        with youtube_dl.YoutubeDL(data.ydl_options) as ydl:
            videos = ydl.extract_info(f"ytsearch5:{arg}", download=False)   # Returns a dictionary with results
            
        # Ensure that "videos" is valid
        if videos is None or "entries" not in videos:
            await ctx.send("No results found.")
            return

        videos = videos["entries"][:5]

        view = discord.ui.View()

        # Loop through results in "videos"
        for index, vid in enumerate(videos):
            vidTitle = vid['title']
            vidUrl = vid['webpage_url']

            # Construction of buttons
            button = discord.ui.Button(
                label=f"{index + 1}.{vidTitle[:40]}",
                style=discord.ButtonStyle.primary
            )

            # Callback after button is clicked
            async def callback(interaction, url=vidUrl):
                global is_searching
                
                await ctx.send(f"**SELECTED VIDEO**: {url}")
                await runplay(ctx, url)    # Call "play" command to play the selected video
                is_searching = False

            button.callback = callback

            # Add button to view
            view.add_item(button)

        await ctx.send("**SELECT VIDEO**", view=view)
        is_searching = False
    except Exception as e:
        await ctx.send(f"An error occurred while searching. Error: {e}")
        return