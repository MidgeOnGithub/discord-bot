## Welcome to Midge's Discord Bot Documentation

### General Info
The code for this bot relies entirely upon the discord.py rewrite module, [which can be found on Github](https://github.com/Rapptz/discord.py/tree/rewrite)
> Vocabulary Notes:
> * Discord refers to "Servers" internally as "Guilds", as does the Discord.py Rewrite
> * Discord.py rewrite code and documentation refers to what is often called a "module" as a "cog"

Currently, this bot is being developed as a personal exercise in dealing with medium-length projects with a specific server and use case in mind.
> The Specific Use Case:
> * Act as a guild helper, giving automated helpful responses to specific commands queued by members attempting to answer newcomer's or their own questions
> * Keep track of everyone in the guild who is streaming and give them a server-specific "Live" role to highlight them among other guild members
  > * This will only be done if the game they are streaming is in a specific game filter list

If the project is enjoyable enough, it may be expanded for general use by others with configurable settings. Settings would include the following:
* Command availability (in case some commands are unnecessary)
* Command permissions (restricting who can use each command or each "category" of commands)
* Command cooldowns (preventing individual or guild-wide spam)
* Optional guild-specific game filter list for the "Live" role implementation

### Code and Command Info
Generally speaking, the code within this project is heartily commented, perhaps in some cases redundantly so.
In the future, this may be changed in favor of placing comment information to the documentation here, instead of "cluttering" the code with comments.
For now, the direction is to check the code itself -- purpose, implementation, and usage should be well documented there
> Current Cog List:
> * bot_management
> * moderation
> * filter_live

### Important Clone/Fork Information
Note that in the root directory of your project (or elsewhere, provided you edit bot.py accordingly) you need a `botcredentials.py` file, which must contain this line:
> `TOKEN = 'YourDiscordDeveloperAppTokenInQuotesEvenThoughItsANumber'`
This is for security. By default, the file `botcredentials.py` will be gitignored if you use this project's `.gitignore` file, preventing the TOKEN from being published anywhere when using git for version control.
Of course, you can create an alternate implementation as you wish.