# EVE-bot
I wanted a Discord bot for EVE, but I didn't want one that could leak sensitive information. So I made my own.

If you find this useful, please tell `spicy indian` in game with a mail and or ISK donation!

## What does EVE-bot do?
This is still a work in progress, and this list will grow.

### Intel Tracking
The primary purpose for EVE-bot is to scrape the alliance intel channel for suspicious activity near our system.

## Usage
1. Download the latest release, and unzip the file.
1. Create the eve-bot.cfg file
1. Run bot.exe
1. Launch EVE. Make sure that you log in __after__ launching the bot, or the bot will not be able to find the files!

### eve-bot.cfg
Here's what to put in eve-bot.cfg. You should not use quotes, unless quotes are used in the example.

To get your own discord bot token, you will need make a bot user.

```
[discord]
token = your discord bot token, no quotes
dev_token = (optional) your discord bot token, prefered over token

[intel]
discord_channel = Discord channel to post intel, no quotes (defaults to general)
eve_channels = [
    "EVE chat channel 1",
    "EVE chat channel 20"]
```
