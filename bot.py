from datetime import datetime

import discord
from discord.ext import commands

import botcredentials

# Set command prefix and a Status indicating initialization
bot = commands.Bot(command_prefix='!',
                   status=discord.Status.idle,
                   activity=discord.Game(name='Booting...'))

# Store the bot's launch time
bot.start_time = datetime.utcnow()

@bot.event
async def on_ready():
    # Once ready, give summary info and change Status
    print(f'Now online as {bot.user}. Ready to go!\n'
          f'Serving {len(bot.guilds)} guilds ' +
          f'with {len(bot.users)} users!')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Active!'))

@bot.event
async def on_message(message):
    # Ignore messages from self, otherwise process as usual
    if message.author == bot.user:
        return
    await bot.process_commands(message)


# A list of cog names: currently requires manual entry
# owner cog contains commands to load and unload extensions
default = ['owner', 'live', 'moderation', 'stats']

# TODO: Optional cogs should be added by configuration/settings
extensions = default

# Only run the bot if this file is __main__
if __name__ == '__main__':
    for ext in extensions:
        try:
            # Assume an unchanged relative path to cog files
            bot.load_extension('cogs.' + ext)
        except (discord.ClientException, ImportError) as err:
            print(f'{ext} not loaded. [{err}]')

# Start the bot
bot.run(botcredentials.TOKEN)
