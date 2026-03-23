# **BASSIPY**

---

## INFO
Bassipy is a locally runnable Discord bot made for playing music in Discord voice channels.
It is written in Python and uses FFmpeg with yt-dlp and discord.py python packages.
Bassipy is supposed to be a simple bot and contains 3 main commands, "play", "skip" and "search". They can be used by typing the prefix(!) following with the command(eg. !search).
The PLAY command takes a youtube link and plays it(eg. !play https://www.youtube.com/watch?v=dQw4w9WgXcQ).  
The SEARCH command searchs the top 5 results of an argument using yt-dlp(eg. !search rap).   
The SKIP command skips/stops the currently playing song.  
The bot does not feature a queue yet and only plays one song at a time. It works by downloading an audio file first and then playing it, which might be an issue for some people because of extra downloads and network traffic. I am planning to move to a streaming approach instead of downloading files.

---

## HOW TO USE (WINDOWS)
### Setting up environment
1. Clone the repository  
 `git clone https://github.com/n1xerii/bassipy.git`
2. Go inside the cloned folder  
 `cd bassipy`
3. Create a new Python environment  
 `conda create -n bassipy python=3.11` or `python -m venv bassipy`
4. Activate the environment  
 `conda activate bassipy` or `venv\Scripts\activate.bat`
5. Install the requirements  
 `pip install -r requirements.txt`

### Setting up bot_data.py
1. Add a new python file "bot_data.py" into the folder
2. Open "bot_data.py" and add two lines: `my_token = ""` and `my_platform = ""`
3. Input your Discord bot token `my_token = "yourtokenhere"` (DISCLAIMER: NEVER SHARE YOUR BOT TOKEN!)
4. Input your platform, in this case its Windows `my_platform = "Windows"`
5. Save the file and you bot_data.py is ready!

### Install deno
1. npm install deno

### Running the bot
1. Open Powershell or CMD.
2. Navigate to the location of your repository `cd path/to/cloned/repo`
3. Run `python run_bot.py` in your terminal and the bot should start!

---
 
