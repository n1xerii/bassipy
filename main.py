import os
import asyncio
import discord
import yt_dlp
from discord import FFmpegOpusAudio, FFmpegAudio, FFmpegPCMAudio

import data

#is_playing = False
is_searching = False

song = None
current_song = None
songs = []

index_count = 0

def get_song(urlToUse, ctx):
    try:
        # Prepare file
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            #info = ydl.extract_info(urlToUse, download=True)

            info = ydl.extract_info(urlToUse, download=False)

            song_url = info['url']
            #ydl.sanitize_info(info)
            #audioFile = ydl.prepare_filename(info)

            return song_url
            #return audioFile
    except Exception as e:
        print(f"--- An error occurred: {e}")
        return None

async def disconnect_from_voice(ctx):
    if data.vc_conn is None:
        return

    await data.vc_conn.disconnect()

# PLAY COMMAND
# | Plays a link from YouTube in a Discord voice channel
async def runplay(ctx):
    global current_song
    global index_count

    try:
        vc_to_join = ctx.author.voice.channel

        # Connect to the voice channel
        if data.vc_conn is None:
            data.vc_conn = await vc_to_join.connect()

        if len(songs) > 0:
            if index_count >= len(songs):
                songs.clear()
                current_song = None
                index_count = 0
                print("--- Clearing songs and resetting index counter.")
                return

            current_song = songs[index_count]
            index_count += 1

        # Making sure file exists before playing / not needed for streaming
        #if not os.path.isfile(current_song):
        #    print(f"Audio file not found: {current_song}")
        #    await ctx.send("Error with audio file!")
        #    return

        #audio_source = FFmpegOpusAudio(current_song, executable=data.ffmpeg)
        #audio_source = FFmpegPCMAudio(current_song, executable=data.ffmpeg)
        #data.vc_conn.play(audio_source)

        audio_source = FFmpegOpusAudio(
            current_song,
            executable=data.ffmpeg,
            **data.ffmpeg_options
        )

        data.vc_conn.play(audio_source)

        while data.vc_conn.is_playing():
            await asyncio.sleep(1)

        await ctx.send("Finished playing song.")
        await asyncio.sleep(1)
        await runplay(ctx)
    except Exception as e:
        print(f"--- An error occurred in runplay: {e}")
        return

# SKIP COMMAND
# | Skips the currently playing song
async def runskip(ctx):
    global current_song
    global index_count

    if not data.vc_conn.is_connected():
        await ctx.send("Not connected to voice channel.")
        return

    if data.vc_conn.is_playing():
        data.vc_conn.stop()

        await ctx.send("Song skipped!")
        await runplay(ctx)
        return

# SEARCH COMMAND
# | Searches 5 top results for "arg" from YouTube and lets user choose which one to play
""" Disabled for clarity
async def runsearch(ctx, *, arg):
    global is_searching
    
    try:
        await ctx.send("Searching... Please wait...")

        is_searching = True
        
        # Call "ytsearch5" from ytdlp and populate "videos" with the result
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
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
                #await runplay(ctx, url)    # Call "play" command to play the selected video / Temporarily disabled
                is_searching = False

            button.callback = callback

            # Add button to view
            view.add_item(button)

        await ctx.send("**SELECT VIDEO**", view=view)
        is_searching = False
    except Exception as e:
        await ctx.send(f"--- An error occurred while searching. Error: {e}")
        return
"""
