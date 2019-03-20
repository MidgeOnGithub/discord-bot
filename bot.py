from datetime import datetime
from glob import glob
from os import path

import discord
from discord.ext import commands

import botcredentials


# TODO: Per-guild prefixes
def _get_prefix(bot, message):
    """
    Get the bot's command prefix.
    """
    prefix = '!'

    # If in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefix)(bot, message)


# TODO: Configurable startup extensions?
def _get_startup_extensions():
    """
    Get the bot's startup cogs.
    """
    # A list of default cog names: currently requires manual entry
    default = [*bot.core_cogs, 'moderation', 'live', 'stats']
    all_extensions = default
    return all_extensions


def _cog_file_available(self, cog):
    """
    Determines if a cog file exists within the program's known directories.
    """
    return cog in self._cog_files()


def _get_cog_files():
    """
    Returns a list of cog files within the program's known directories.
    """
    cogs = [path.basename(f) for f in glob("cogs/*.py", recursive=True)]
    return [f[:len(f)-3] for f in cogs]


# Set command prefix and a Status indicating initialization
bot = commands.Bot(command_prefix=_get_prefix, status=discord.Status.idle,
                   activity=discord.Game(name='Booting...'))

bot.core_cogs = ('owner', 'error_handler')

# Store the bot's launch time
bot.start_time = datetime.utcnow()


@bot.event
async def on_ready():
    # Once ready, give summary info and change Status
    print(f'Now online as {bot.user}. Ready to go!\n'
          f'Serving {len(bot.guilds)} guilds with {len(bot.users)} users!')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Active!'))

# TODO: Optional cogs should be added by configuration/settings
extensions = _get_startup_extensions()

for ext in extensions:
    try:
        bot.load_extension('cogs.' + ext)
    except commands.ExtensionError as err:
        print({err})

# Don't bother starting if one of the core cogs fails to load
if not all(cog in [cog[5:] for cog in set(bot.extensions.keys())] for cog in bot.core_cogs):
    exit(1)

bot.mod_cog = bot.get_cog('Moderation')

# Start the bot
bot.run(botcredentials.TOKEN, bot=True, reconnect=True)
