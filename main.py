import os
import asyncio
import discord
import yt_dlp
from discord import FFmpegOpusAudio

import data

is_playing = False
is_searching = False

song = None
songs = []

def get_song_data(urlToUse):
    try:
        # Prepare file
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            info = ydl.extract_info(urlToUse, download=True)
            #audioFile = ydl.prepare_filename(info)

            ydl.sanitize_info(info)

            audioFile = ydl.prepare_filename(info)
            # errorCode = ydl.download(urlToUse)

            return audioFile
    except Exception as e:
        #logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return None

async def disconnect_from_voice(ctx):
    global is_playing

    if data.vc_conn is None:
        return

    await data.vc_conn.disconnect()

# PLAY COMMAND
# | Plays a link from Youtube in a Discord voice channel
async def runplay(ctx, url: str):
    global is_playing
    global song

    # If user is not in a voice channel, prompt to join one
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first!")
        return

    song = get_song_data(url)
    #songs.append(song)

    try:
        vc_to_join = ctx.author.voice.channel

        # Connect to the voice channel
        data.vc_conn = await vc_to_join.connect()

        # Making sure file exists before playing
        if not os.path.isfile(song):
            await ctx.send(f"Audio file not found: {song}")
            return

        #is_playing = True

        audio_source = FFmpegOpusAudio(song, executable=data.ffmpeg)
        data.vc_conn.play(audio_source)

        while data.vc_conn.is_playing():
            await asyncio.sleep(1)

        #for songToPlay in songs:

            # Prepare audio source
            #audio_source = FFmpegOpusAudio(songToPlay, executable=data.ffmpeg)

            # Play audio source in voice channel
            #data.vc_conn.play(audio_source)

            # Keep playing the song until it ends
            #while data.vc_conn.is_playing():
            #    await asyncio.sleep(1)

            # Delete audio file
            #os.remove(songToPlay)

        #songs.clear()

        # Set is_playing to false to allow running play command again / deprecated comment
        #is_playing = False

        await disconnect_from_voice(ctx)
        await ctx.send("Finished playing audio.")
    except Exception as e:
        #logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return


# SKIP COMMAND
# | Skips the currently playing song
async def runskip(ctx):
    global is_playing

    # If audio is playing, skip the current song and disconnect
    if data.vc_conn is not None:
        data.vc_conn.stop()
        await ctx.send("Song skipped!")
        await disconnect_from_voice(ctx)

        is_playing = False
        return


# SEARCH COMMAND
# | Searches 5 top results for "arg" from Youtube and lets user choose which one to play
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