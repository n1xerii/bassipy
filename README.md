# **BASSIPY**

---

## INFO
Bassipy is a locally running Discord bot made for playing music in voice channels.
It uses 'discord.py' and 'yt-dlp' and is written in Python.
Bassipy is supposed to be a simple bot and only features 3 main commands, "play", "skip" and "search". The command can be used by typing the prefix(!) following with the command(eg. !search).
The PLAY command takes a youtube link and plays it(eg. !play https://www.youtube.com/watch?v=dQw4w9WgXcQ), or if a song is already playing, it adds the song to the queue.
The SEARCH command searchs the top 5 results of an argument using yt-dlp(eg. !search rap).
The SKIP command skips/stops the currently playing song.

---

## HOW TO USE
### Setting up environment
1. Clone the repository
 `git clone https://github.com/n1xerii/bassipy.git`
2. Go inside the cloned folder
 `cd bassipy`
3. Create a new Python environment (I recommend conda)
 `conda create -n bassipy python=3.11` or `python -m venv bassipy`
4. Activate the environment
 `conda activate bassipy` or `venv\Scripts\activate.bat`
5. Install the requirements
 `pip install -r requirements.txt`

### Setting up bot_data.py
1. Add a new python file "bot_data.py" into the folder
2. Open "bot_data.py" and add one line: `my_token = ""`
3. Add your Discord bot token `my_token = "yourtokenhere"` (DISCLAIMER: NEVER SHARE YOUR TOKEN!)
4. Save the file and your bot_data.py is ready!

### Install deno
1. Install node.js for Windows from (https://nodejs.org/en/download) 
2. Run `npm install deno` in Powershell or CMD

### Running the bot
1. Open Powershell or CMD.
2. Navigate to your bassipy repository `cd path/to/folder`
3. Run `python run_bot.py` in your terminal and the bot should start!

---
 
