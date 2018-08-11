# Discord-infosec
get info,channels, messages from servers , discord.py
**simple** code(bot) for get info from servers , using discord.py

If someone invited your bot to his server,or you invited a stranger bot to your server 
What information can collect? This is the goal I want to clarify to you

**NOTE: only to explain the risk of the bots, And what they can do!! , NOTE+1: can do more than this code :)**


## Features
- all & voice channels (including hidden channels).
- who in voice channel (including hidden channel).
- save last 1500 messages from all text channel (read_messages permissions).
- creates invite link (createـinvite permission).


## Requirements
- python 3.6.X
- pip

**modules :**
- discord.py 
`pip3 install discord.py` or for windows `py -m pip install -U discord.py`



## Token&Prefix
open `infosec.py` go to [line 17 & 18] :
```
prefix = "!"
token = "Token Here"
```
replace perfix as you like and token by your own

### Start the bot
 - **Linux and macOS :** `python3 infosec.py` 
 - **Windows :** `py infosec.py`
 
 
### Commands 
> help command : !h

available commands :
```
!inv : Get an invite from choosen server
!chatlog : Save last 1500 messages from all chats
!tc = Get all text channels
!vm = Get all voice channels with members```
```

 ## Who am i ?
 Ahmad A. Alsrehy
 
 Twitter : [@ADsecu](http://twitter.com/adsecu) 
 
