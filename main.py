import asyncio
import yt_dlp
import discord
from discord import FFmpegOpusAudio

import data

is_searching = False

current_song = None
songs = []

index_count = 0

def get_song_data(song_url, ctx):
    try:
        # Prepare song url
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            info = ydl.extract_info(song_url, download=False)

            song_info = info

            return song_info
    except Exception as e:
        print(f"--- [BASSIPY] : An error occurred in get_song: {e}")
        return None

def add_song_to_queue(song):
    songs.append(song)

async def disconnect_from_voice(ctx):
    if data.vc_conn is None or data.vc_conn.is_connected():
        return

    await data.vc_conn.disconnect()

# PLAY COMMAND
# | Plays a link from YouTube in a Discord voice channel
async def song_player(ctx):
    global current_song
    global index_count

    try:
        if len(songs) > 0:
            """ OLD SYSTEM
            if index_count >= len(songs):
                current_song = None
                songs.clear()
                index_count = 0
                print("--- [BASSIPY] : Queue finished. Clearing songs and resetting song index.")
                await ctx.send("Finished playing.")
                return

            #current_song = songs[index_count]
            #index_count += 1
            #print(f"--- [BASSIPY] : Song: {current_song['title']}")
            """
            # NEW SYSTEM
            current_song = songs[0]
            print(f"--- [BASSIPY] : Song: {current_song['title']}")
        else:
            current_song = None
            songs.clear()
            await ctx.send("Queue finished.")
            print(f"--- [BASSIPY] : Queue finished.")
            return

        if current_song is None:
            print(f"--- [BASSIPY] : Error occurred with song url: {current_song['url']}")
            await ctx.send(f"Unknown error with song url:  {current_song['url']}")
            return

        audio_source = FFmpegOpusAudio(
            current_song['url'],
            executable=data.ffmpeg,
            **data.ffmpeg_options
        )

        data.vc_conn.play(audio_source)

        while data.vc_conn.is_playing():
            await asyncio.sleep(1)

        if len(songs) > 0:
            songs.remove(current_song)

        await asyncio.sleep(0.5)
        await song_player(ctx)
    except Exception as e:
        print(f"--- [BASSIPY] : An error occurred in play: {e}")
        return


# SKIP COMMAND
# | Skips the currently playing song
async def song_skipper(ctx):
    global current_song

    if data.vc_conn.is_playing():
        data.vc_conn.stop()

        songs.remove(current_song)
        current_song = None
        
        await ctx.send("Song skipped!")
        await song_player(ctx)
        return
    else:
        await ctx.send("Not playing a song.")


# SEARCH COMMAND
# | Searches 5 top results for "arg" from YouTube and lets user choose which one to play
async def song_searcher(ctx, *, arg):
    global is_searching
    
    try:
        await ctx.send("Searching... Please wait...")

        is_searching = True
        
        # Use ytdlp to fetch 5 songs
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            videos = ydl.extract_info(f"ytsearch5:{arg}", download=False)
        
        # Ensure that the songs are valid
        if videos is None or "entries" not in videos:
            await ctx.send("No results found.")
            return

        videos = videos["entries"][:5]

        view = discord.ui.View()

        # Loop through the songs
        for index, vid in enumerate(videos):
            vidTitle = vid['title']
            vidUrl = vid['webpage_url']

            # Make buttons
            button = discord.ui.Button(
                label=f"{index + 1}.{vidTitle[:40]}",
                style=discord.ButtonStyle.primary
            )

            # Button click/callback
            async def callback(interaction, url=vidUrl):
                global is_searching
                
                await ctx.send(f"**SELECTED VIDEO**: {url}")
                selected_song = get_song_data(url)
                is_searching = False
                return selected_song
                #await song_player(ctx)
            button.callback = callback

            # Add button to view
            view.add_item(button)

        await ctx.send("**SELECT VIDEO**", view=view)
        is_searching = False
    except Exception as e:
        await ctx.send(f"--- An error occurred with search: {e}")
        return
