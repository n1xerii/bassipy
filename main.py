import asyncio
import yt_dlp
from discord import FFmpegOpusAudio

import data

is_searching = False

song = None
current_song = None
songs = []

index_count = 0

def get_song(urlToUse, ctx):
    try:
        # Prepare song url
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            info = ydl.extract_info(urlToUse, download=False)

            song_url = info['url']

            return song_url
    except Exception as e:
        print(f"--- [BASSIPY] : An error occurred in get_song: {e}")
        return None

async def disconnect_from_voice(ctx):
    if data.vc_conn is None or data.vc_conn.is_connected():
        return

    await data.vc_conn.disconnect()

# PLAY COMMAND
# | Plays a link from YouTube in a Discord voice channel
async def runplay(ctx):
    global current_song
    global index_count

    try:
        if len(songs) > 0:
            if index_count >= len(songs):
                current_song = None
                songs.clear()
                index_count = 0
                print("--- [BASSIPY] : Queue finished. Clearing songs and resetting song index.")
                await ctx.send("Finished playing.")
                return

            current_song = songs[index_count]
            index_count += 1
            print(f"--- [BASSIPY] : current_song: {current_song}")

        if current_song is None:
            print(f"--- [BASSIPY] : error occurred with song url: {current_song}")
            await ctx.send("Unknown error occurred with song url.")
            return

        audio_source = FFmpegOpusAudio(
            current_song,
            executable=data.ffmpeg,
            **data.ffmpeg_options
        )

        data.vc_conn.play(audio_source)

        while data.vc_conn.is_playing():
            await asyncio.sleep(1)

        await ctx.send("Starting next song.")
        await asyncio.sleep(1)
        await runplay(ctx)
    except Exception as e:
        print(f"--- [BASSIPY] : An error occurred in runplay: {e}")
        return

# SKIP COMMAND
# | Skips the currently playing song
async def runskip(ctx):
    global current_song
    global index_count

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
