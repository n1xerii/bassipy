# **BASSIPY**

---

## INFO
Bassipy is a local Discord bot made for playing music in voice channels.
It uses Ffmpeg and Python with "yt-dlp" and "discord.py" packages.  
Bassipy is currently a very simple bot(although I am trying to expand it whenever I can) and there are only 3 song commands, "play", "skip" and "search". They can be used by typing the prefix(!) following with the command(eg. !search).
The PLAY command takes a youtube link and plays it(eg. !play https://www.youtube.com/watch?v=dQw4w9WgXcQ).  
The SEARCH command takes an argument and searches for the top 5 results of it(eg. !search rap).   
The SKIP command just skips the currently playing song.  
The bot does not yet feature a queue and only plays one song at a time.

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
1. Add a new python file named "bot_data.py" into the root folder of the repository
2. Open "bot_data.py" and add these two lines: `my_token = ""` and `my_platform = ""`
3. Input your Discord bot token `my_token = "yourtokenhere"`
4. Input your platform, in this case its Windows `my_platform = "Windows"`
5. Save the file and you bot_data.py is ready!

### Running the bot
1. Open a terminal or a CMD prompt.
2. Navigate to the location of your repository `cd path/to/cloned/repo`
3. Run `python run_bot.py` in your terminal or CMD and the bot should start!

---
 
