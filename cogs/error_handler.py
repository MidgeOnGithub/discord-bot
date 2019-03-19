import traceback
import sys
import discord
from discord.ext import commands

"""
Adapted from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
"""


class ErrorHandler(commands.Cog):
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

        ignored = commands.CommandNotFound
        standard_notification = (
            commands.CheckFailure, commands.NotOwner,
            commands.UserInputError, commands.CommandOnCooldown
        )

        # Check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found, keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return
        # TODO: Create more specific messages for some things currently
        #  handled in standard_notification
        elif isinstance(error, standard_notification):
            if isinstance(error, commands.MissingRequiredArgument):
                return await ctx.send(f'Required argument `{error.param}` not given.')
            return await ctx.send(f'{error.args[0]}.')
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} is disabled.')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} cannot be used in DMs.')
            except discord.DiscordException as ex:
                print(f'{ex.args[0]}.')

        # If not handled above, print default traceback.
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error,
                                  error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
