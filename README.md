# cowsaybot
A discord bot that puts messages in a cowsay  
invite link: https://discordapp.com/api/oauth2/authorize?client_id=627468031110414355&permissions=68608&scope=bot

#### Requirements:
- discord.py
- cowsay installed on host

#### Setup:
1. Make a discord developer app
2. Add a bot to this app
3. Copy the **bot token** and put it in bot.secret

### Functionality:
The bot will put any message starting with `cow ` in a cowsay
for example, saying 
>cow moo

will result in
```
 _____
< moo >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
Every time a new message is sent in the server, the bot will randomly generate a number between 0 & 501.  
If this number is 1, it will put the message in a cowsay on its own, just to keep things interesting.  
(I do recommend blocking the bot from talking in vent & other serious channels)


to start the bot, just invite it & run main.py  
(invites must be generated on the discord developer page)
