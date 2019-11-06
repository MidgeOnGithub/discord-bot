import datetime
import glob
import logging
import os
from pathlib import Path

import aiohttp
import asyncio
import discord
from discord.ext import commands

from utils.db import Table
from utils import data_io

from botcredentials import TOKEN, PGSQL


# TODO: Per-guild prefixes
def get_prefix(bot, message):
    """
    Get the bot's command prefix(es).
    """
    default = '!'
    if not message.guild:
        return default

    prefixes = set(default)
    # for prefix in settings.prefixes:
    #     prefixes.add(prefix)

    return commands.when_mentioned_or(*prefixes)(bot, message)


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


logging.basicConfig(level=logging.INFO)

# loop = asyncio.get_event_loop()
# try:
#     pool = loop.run_until_complete(Table.create_pool(PGSQL, command_timeout=60))
# except Exception:
#     exit(1)


# Set command prefix and a Status indicating initialization
bot = commands.AutoShardedBot(command_prefix=get_prefix, status=discord.Status.idle,
                              activity=discord.Game(name='Booting...'))
# Store the bot's launch time
bot.start_time = datetime.datetime.utcnow()
# bot.pool = pool
bot.core_cogs = ('admin', 'error_handler')

extensions = [*bot.core_cogs, 'moderation', 'live', 'stats', 'twitch']

for ext in extensions:
    try:
        bot.load_extension('cogs.' + ext)
    except commands.ExtensionError as err:
        print({err})

# Don't bother starting if a core cog fails to load
if not all(cog in [cog[5:] for cog in set(bot.extensions.keys())] for cog in bot.core_cogs):
    exit(1)


@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    # Once ready, give summary info and change Status
    print(f'Now online as {bot.user}. Ready to go!\n'
          f'Serving {len(bot.guilds)} guilds with {len(bot.users)} users!')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Active!'))

# Start the bot
bot.run(TOKEN, bot=True, reconnect=True)
