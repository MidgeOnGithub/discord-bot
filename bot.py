import datetime
import glob
import os
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands

import utils.data_io

from botcredentials import TOKEN


# TODO: Per-guild prefixes
def get_prefix(bot, message):
    """
    Get the bot's command prefix(es).
    """
    default = '!'
    if not message.guild:
        return default

    prefixes = set(default)
    for prefix in settings.prefixes:
        prefixes.add(prefix)

    return commands.when_mentioned_or(*prefixes)(bot, message)


# TODO: Configurable startup extensions?
def _get_startup_extensions():
    """
    Get the bot's startup cogs.
    """
    # A list of default cog names: currently requires manual entry
    default = [*bot.core_cogs, 'moderation', 'live', 'stats']
    all_extensions = default
    return all_extensions


def cog_file_available(self, cog):
    """
    Determines if a cog file exists within the program's known directories.
    """
    return cog in self._cog_files()


def get_cog_files():
    """
    Returns a list of cog files within the program's known directories.
    """
    cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py", recursive=True)]
    return [f[:len(f)-3] for f in cogs]


settings_file_location = 'data/settings.json'
if not Path(settings_file_location).is_file():
    utils.data_io.generate_default_settings(settings_file_location)
settings = utils.data_io.load_settings(settings_file_location)

# Set command prefix and a Status indicating initialization
bot = commands.Bot(command_prefix=get_prefix, status=discord.Status.idle,
                   activity=discord.Game(name='Booting...'))

bot.core_cogs = ('settings', 'owner', 'error_handler')

# Store the bot's launch time
bot.start_time = datetime.datetime.utcnow()


@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    # Once ready, give summary info and change Status
    print(f'Now online as {bot.user}. Ready to go!\n'
          f'Serving {len(bot.guilds)} guilds with {len(bot.users)} users!')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Active!'))

extensions = _get_startup_extensions()

for ext in extensions:
    try:
        bot.load_extension('cogs.' + ext)
    except commands.ExtensionError as err:
        print({err})

# Don't bother starting if a core cog fails to load
if not all(cog in [cog[5:] for cog in set(bot.extensions.keys())] for cog in bot.core_cogs):
    exit(1)

bot.settings = settings
bot.settings_file = settings_file_location

# Start the bot
bot.run(TOKEN, bot=True, reconnect=True)
