import os

import discord
from discord.ext import commands

import botcredentials

# Set command prefix and a Status indicating initialization
client = commands.Bot(command_prefix='!',
                      status=discord.Status.idle,
                      activity=discord.Game(name='Booting...'))
client.remove_command('help')

# Once ready, give summary info and change Status
@client.event
async def on_ready():
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


@client.command()
async def user(ctx, target: discord.Member = None):
    # Determine who is the target, set pronouns accordingly
    # If no target is specified, invoking member is target
    if target == None:
        target = ctx.message.author
        p1, p2 = 'Your', 'You'
    elif target.bot:
        p1, p2 = 'Its', 'It'
    else:
        p1, p2 = 'Their', 'They'
    # Determine certain properties and text regarding the user
    nick = target.display_name
    username = f'{target.name}#{target.discriminator}'
    join_time = target.joined_at
    # Point out a member's top role if they have one beyond @everyone
    if len(target.roles) != 1:
        role = target.top_role
        r_msg = f'{p1} top role is {role}.'
    else:
        ## Using this message prevents pinging @everyone
        r_msg = f'{nick} has no special roles.'
    # Point out if the member is a bot
    if target.bot:
        bot_msg = f'\n{nick} is a bot.'
    else:
        bot_msg = ''
    # Send the message
    await ctx.channel.send(f'{nick}\'s full username is {username}.\n{p2} joined at {join_time}.\n{r_msg}{bot_msg}')

# A list of cog names: currently requires manual and edits
# bot_management cog contains commands to load and unload extensions
## Could automate, e.g., search all of __main__'s sub-directories
### This list should generate from configuration/settings
extensions = ['bot_management',
              'live',
              'moderation']

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
