from datetime import datetime

import discord
from discord.ext import commands

import botcredentials

# Set command prefix and a Status indicating initialization
client = commands.Bot(command_prefix='!',
                      status=discord.Status.idle,
                      activity=discord.Game(name='Booting...'))
client.remove_command('help')
# Store the bot's launch time for use in stats like uptime
client.launch_time = datetime.utcnow()

@client.event
async def on_ready():
    # Once ready, give summary info and change Status
    print(f'Now online as {client.user}. Ready to go!')
    print(f'Serving {len(client.guilds)} guilds with a combined {len(client.users)} users!')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(name='Active!'))


@client.event
async def on_message(message):
    # Ignore messages from self, otherwise process as usual
    if message.author == client.user:
        return
    await client.process_commands(message)


# A list of cog names: currently requires manual and edits
# bot_management cog contains commands to load and unload extensions
## Could automate, e.g., search all of __main__'s sub-directories
### This list should generate from configuration/settings
extensions = ['bot_management',
              'live',
              'moderation',
              'stats']

# Only run the bot if this file is __main__ (is not imported)
## This should prevent setup.py/settings file(s) from starting the bot
if __name__ == '__main__':
    for ext in extensions:
        try:
            # Assume an unchanged relative path to cog files
            client.load_extension('cogs.' + ext)
        except (discord.ClientException, ImportError) as err:
            print(f'{ext} not loaded. Check it exists and has a `setup` function. [{err}]')

# Start the bot client
client.run(botcredentials.TOKEN)
