# Epic-Gamer

This is a discord bot I stopped working on. Feel free to fork it and use it just be sure to give credit to me if you choose to. For the most part it should work fine, there are only database issues because I made it specifically for my computer.

## Features
All the custom features with this bot are located in `/extensions/`

Current list of extensions:
 - `/extensions/config.py`: An extension for managing server settings such as a custom prefix
 - `/extensions/developer.py`: A bunch of useful developer commands
 - `/extensions/eco.py`: Custom economy system, inspured off of Dank Memer but it's a lot smaller
 - `/extensions/fun.py`: Random and harmless fun commands
 - `/extensions/help.py`: The help command, commands are automatically added as you add more
 - `/extensions/logs.py`: Server logging for mods and admins
 - `/extensions/manipulation.py`: Text manipulation
 - `/extensions/mod.py`: Moderation commands that are semi useful
 - `/extensions/modmail.py`: A basic modmail extension that lets users DM the bot and report it to the correct channel
 - `/extensions/utility.py`: Useful comnmands for statistics and server owners
 - `/extensions/utils/error.py`: A custom error handler that reports the common errors into the correct text channel

## Installation
 - Install Python 3.8 or higher 
 - Clone the repository:
 ```git clone https://github.com/NatFletch/Epic-Gamer.git```
 - Open a terminal in the directory you cloned the repo and run:
 ```python3 -m pip install -U -r requirements.txt```
 - Once done make a file called `secret.py` and paste the following contents
 ```secret.py
 token = "your bot token here"
 password = "your postgres password here"
 ```
 - After that run `python3 index.py` and you should be good to go

###### This code is not compatible with Discord.py 2.x and I do not plan to migrate it anytime soon. If you don't want to make any major changes to code then wait until I get around to releasing Epic Gamer 2 (a rewrite basically)
