## Welcome to Midge's Discord Bot Documentation

### General Info
The code for this bot is built upon the discord.py library, [which can be found on Github](https://github.com/Rapptz/discord.py/tree/rewrite).
> Vocabulary Notes:
> * Discord refers to "Servers" internally as "Guilds", as does the Discord.py documentation
> * Discord.py rewrite refers to what is often called a "module" or "extension" as a "cog"

The inspiration for the bot is a personal challenge in learning/conforming to the heart of PEP-8 standards while dealing with a medium-length project.
The bot is initially being developed with a specific guild and use case in mind.
> Specific Use Case:
> * Act as a guild helper for the Tomb Runner Discord guild, giving automated helpful responses to commands invoked by members attempting to answer newcomers' (or their own) questions
> * Keep track of everyone in the guild who is streaming and give them a guild-specific "Live" role to highlight them among other guild members
  >   * This can be restricted by a game filter list (exceptions for users in whitelists or blacklists)

If the project is enjoyable enough, it may be expanded for general use by others with configurable settings.
> (Potential) Configurable Settings:
> * Command availability (some commands may be unnecessary or undesired in certain guilds)
> * Command permissions by roles (restricting who can use each command or each "category" of commands)
> * Command cooldown timings (preventing individual or guild-wide spam)
> * Optional guild-specific game filter list for "Live" role implementation
  >   * Optional guild whitelist allowing users to be exempt from said filter
  >   * Optional guild blacklist allowing users to be excluded from the live role completely

### Code and Command Info
Generally speaking, the code within this project should be readable, commented where it's not.
For now, the direction is to check the code itself -- purpose, implementation, and usage should be intuitive (I hope).
> Current Cog List:
> * 'Core':
  >   * error_handler
  >   * admin
  >   * settings
> * live
> * moderation
> * stats
> * twitch

### Important Clone/Fork Information
In order to run this bot, in the root directory of your project you need a `botcredentials.py` file with this code:
> * `TOKEN = 'YourDiscordDevAppTokenInQuotes'`
> (optionally, if using the `Twitch` cog):
> * `TWITCH_CLIENT_ID = 'YourTwitchAppClientIDInQuotes'`

This is for security.
By default, the file `botcredentials.py` will be git-ignored if you use this project's `.gitignore` file, preventing TOKEN and/or TWITCH_CLIENT_ID from being published anywhere when using git for version control.
Of course, you can use an alternate implementation as you wish.
