## Welcome to Midge's Discord Bot Documentation

### General Info
The code for this bot relies heavily upon the discord.py rewrite module, [which can be found on Github](https://github.com/Rapptz/discord.py/tree/rewrite).
> Vocabulary Notes:
> * Discord refers to "Servers" internally as "Guilds", as does the Discord.py Rewrite
> * Discord.py rewrite refers to what is often called a "module" or "extension" as a "cog"

The inspiration for the bot is a personal challenge in learning/conforming to the heart of PEP-8 standards while dealing with a medium-length project.
The bot is being developed with a specific server and use case in mind.
> Specific Use Case:
> * Act as a guild helper, giving automated helpful responses to specific commands queued by members attempting to answer newcomer's or their own questions
> * Keep track of everyone in the guild who is streaming and give them a server-specific "Live" role to highlight them among other guild members
  >   * This can be restricted by a game filter list (exceptions for users in whitelists or blacklists)

If the project is enjoyable enough, it may be expanded for general use by others with configurable settings.
> (Potential) Configurable Settings:
> * Command availability (some commands may be unnecessary or undesired in certain guilds)
> * Command permissions by roles (restricting who can use each command or each "category" of commands)
> * Command cooldown timings (preventing individual or guild-wide spam)
> * Optional guild-specific game filter list for "Live" role implementation
  >   * Optional whitelist allowing users to be exempt from said filter
  >   * Optional blacklist allowing users to be excluded from said filter

### Code and Command Info
Generally speaking, the code within this project should be readable, commented where it's not.
For now, the direction is to check the code itself -- purpose, implementation, and usage should be intuitive (I hope).
> Current Cog List:
> * 'Core':
  >   * error_handler
  >   * owner
  >   * moderation
> * live
> * stats

### Important Clone/Fork Information
In order to run this bot, in the root directory of your project you need a `botcredentials.py` file with this code:
> `TOKEN = 'YourDiscordDevAppTokenInQuotesEvenThoughItsANumber'`

This is for security.
By default, the file `botcredentials.py` will be git-ignored if you use this project's `.gitignore` file, preventing TOKEN from being published anywhere when using git for version control.
Of course, you can use an alternate implementation as you wish.
