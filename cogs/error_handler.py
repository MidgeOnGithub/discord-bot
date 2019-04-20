import traceback
import sys

import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    """
    A cog which gives default responses to certain exceptions.
    Adapted from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Event triggered when an error is raised during a command.
        """

        # Prevent commands with local handlers being handled here.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.CheckFailure)
        standard_notification = (commands.NotOwner, commands.UserInputError,
                                 commands.CommandOnCooldown)

        # Check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found, keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return
        elif isinstance(error, discord.HTTPException):
            return await ctx.send(f'An HTTP exception occurred... try again later!')
        elif isinstance(error, standard_notification):
            if isinstance(error, commands.MissingRequiredArgument):
                return await ctx.send(f'Required argument `{error.param}` not given.')
            return await ctx.send(f'{error}')
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} is disabled.')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} cannot be used in DMs.')
            except discord.DiscordException as ex:
                print(f'Discord exception occurred:\n{ex}')

        # If not handled above, print default traceback.
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error,
                                  error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
