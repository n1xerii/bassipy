import os
import main
import data
import bot_data

@data.bot.command()
async def play(ctx, url: str):
    #if main.is_playing:
    #    await ctx.send("Wait for current song to end.")
    #    return
    #if main.is_searching:
    #    await ctx.send("Cant play while searching.")
    #    return

    await main.runplay(ctx, url)

@data.bot.command()
async def skip(ctx):
        if main.is_searching:
            return

        if not main.is_playing:
            await ctx.send("No song to skip.")
            return

        await main.runskip(ctx)

@data.bot.command()
async def search(ctx, *, arg):
    try:
        if main.is_playing:
            await ctx.send("Cant search while playing.")
            return
        if main.is_searching:
            await ctx.send("Already searching.")
            return

        # Temporarily disabled for clarity
        #await main.runsearch(ctx, arg=arg)
    except Exception as e:
        await ctx.send(f"An error occurred. Error: {e}")
        return

@data.bot.command()
async def ping(ctx):
    try:
        await ctx.send(f'Pong! Latency is {round(data.bot.latency * 1000)}ms')
    except Exception as e:
        await ctx.send("An error occurred.")
        print(f"An error occurred. Error: {e}")
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