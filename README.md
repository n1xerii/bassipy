# **BASSIPY**

---

## INFO
Bassipy is a self-hosted, easy to use Discord bot for playing music in voice channels.
It is written in Python and uses `discord.py` and `yt-dlp`.

## COMMANDS
Bassipy is meant to be easy to use and features a small amount of commands. They can be used by typing the prefix(!) following with the command(eg. !play).

`PLAY`  
Plays a link from Youtube(eg. !play https://www.youtube.com/watch?v=dQw4w9WgXcQ). If a song is already playing, it adds the requested song to queue. 

`SKIP`  
Skips current song.

`SEARCH`  
Takes an argument and searches top 5 results for it(eg. !search rap).

'QUEUE'  
Shows songs in queue.

---

## HOW TO USE
### Prepare environment
1. Clone the repository
 `git clone https://github.com/n1xerii/bassipy.git`
2. Go inside the cloned folder
 `cd bassipy`
3. Create a new Python environment (I recommend using conda)
 `conda create -n bassipy python=3.11` or `python -m venv bassipy`
4. Activate the environment
 `conda activate bassipy` or `venv\Scripts\activate.bat`
5. Install the requirements
 `pip install -r requirements.txt`

### Bot data
1. Inside the folder, add a new python file and name it "bot_data.py"
2. Open the file and add your Discord bot token `my_token = "yourtokenhere"` (DISCLAIMER: NEVER SHARE YOUR TOKEN!)
3. Save the file and exit

### Install deno
1. Install node.js for Windows from (https://nodejs.org/en/download). For Linux use your package manager
2. Run `npm install deno` in your terminal(CMD or Powershell on Windows)

### Running the bot
1. Open your terminal(CMD or Powershell on Windows)
2. Navigate to your bassipy repository `cd path/to/folder`
3. Run `python run_bot.py` and the bot should start!

---
 
