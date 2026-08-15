import asyncio
import yt_dlp
import discord
from discord import FFmpegOpusAudio

import data

is_searching = False

current_song = None
songs = []

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

async def add_song_to_queue(song, ctx):
    songs.append(song)
    await ctx.send("Added song to queue!")

async def disconnect_from_voice(ctx):
    if data.vc_conn is None or data.vc_conn.is_connected():
        return

    await data.vc_conn.disconnect()

# PLAY COMMAND
# | Plays a link from YouTube in a Discord voice channel
async def song_player(ctx):
    global current_song

    try:
        if len(songs) > 0:
            current_song = songs[0]
            await ctx.send(f"Playing: {current_song['title']}")
            print(f"--- [BASSIPY] : Song: {current_song['title']}")
        else:
            current_song = None
            songs.clear()
            print("--- [BASSIPY] : Queue finished.")
            await ctx.send("Queue finished.")
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
        await ctx.send(f"An unknown error occurred.")
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
        await ctx.send("Searching...")

        is_searching = True
        
        # Use ytsearch5 from yt-dlp to get 5 songs
        with yt_dlp.YoutubeDL(data.ydl_options) as ydl:
            extracted_songs = ydl.extract_info(f"ytsearch5:{arg}", download=False)
        
        # Ensure songs are valid
        if extracted_songs is None or "entries" not in extracted_songs:
            await ctx.send("No results found.")
            return

        extracted_songs = extracted_songs["entries"][:5]

        view = discord.ui.View()

        # Loop through the songs
        for index, vid in enumerate(extracted_songs):
            song_title = vid['title']
            song_url = vid['webpage_url']

            # Make buttons
            button = discord.ui.Button(
                label=f"{index + 1}.{song_title[:40]}",
                style=discord.ButtonStyle.primary
            )

            # Button click/callback
            async def callback(interaction, url=song_url):
                selected_song = get_song_data(url, ctx)

                await ctx.send(f"**SELECTED SONG**: {selected_song['title']}")
                await add_song_to_queue(selected_song, ctx)

                if not data.vc_conn.is_playing():
                    view.clear_items()
                    await interaction.response.edit_message(view=view)
                    await song_player(ctx)

            button.callback = callback

            # Add button to view
            view.add_item(button)

        await ctx.send(f"**SEARCH** *(requested by {ctx.author})*", view=view)
        is_searching = False
    except Exception as e:
        print(f"Error in search: {e}")
        is_searching = False
        await ctx.send(f"An unknown error occurred.")
        return
