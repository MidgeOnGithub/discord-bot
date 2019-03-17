from datetime import datetime

import discord
from discord.ext import commands

import botcredentials


# TODO: Per-guild prefixes
def get_prefix(bot, message):
    """Get the bot's command prefix."""
    prefix = '!'

    # If in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefix)(bot, message)


# TODO: Configurable extensions?
def get_extensions():
    # A list of default cog names: currently requires manual entry
    default = ['owner', 'error_handler', 'moderation', 'live', 'stats']
    all_extensions = default
    return all_extensions


def main():
    # Set command prefix and a Status indicating initialization
    bot = commands.Bot(command_prefix=get_prefix, status=discord.Status.idle,
                       activity=discord.Game(name='Booting...'))

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
    extensions = get_extensions()

    # Only run the bot if this file is __main__
    for ext in extensions:
        try:
            # Assume an unchanged relative path to cog files
            bot.load_extension('cogs.' + ext)
        except (discord.ClientException, ImportError) as err:
            print(f'{ext} not loaded. [{err}]')

    # Start the bot
    bot.run(botcredentials.TOKEN, bot=True, reconnect=True)


if __name__ == '__main__':
    main()
