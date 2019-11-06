from typing import Union
from copy import copy

import discord
from discord.ext import commands

from utils import checks


class Admin(commands.Cog):
    """Admin-only actions for core bot functionalities and features."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return checks.is_admin()

    @commands.command(hidden=True)
    async def cogs(self, ctx):
        """
        Retrieve the list of loaded cogs.

        Required Permissions:
        Bot owner or admin only.

        Command Usage:
        `cogs`
        """
        cogs = [cog[5:] for cog in self.bot.extensions.keys()]
        await ctx.send(f'Loaded cogs:\n```{cogs}```')

    @commands.command(hidden=True)
    async def load(self, ctx, cog: str):
        """
        Load a cog.

        Required Permissions:
        Bot owner only.

        Command Usage:
        `load <cog>`
        """
        if cog == 'live':
            await ctx.send('I need the `manage_roles` permission for this cog to work properly.')
            # TODO: see print below
            print('DEV NOTE (load in owner)):'
                  'Change this message to a check in an eventual `enable` command in moderation cog.')
        try:
            self.bot.load_extension('cogs.' + cog)
        except commands.ExtensionError as err:
            return await ctx.send(err)
        await ctx.send(f'{cog} loaded.')

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str):
        """
        Unload a cog, unless it is a core cog.

        Required Permissions:
        Bot owner or admin only.

        Command Usage:
        `unload <cog>`
        """
        if cog in self.bot.core_cogs:
            return await ctx.send(f'{cog} cannot be unloaded!')
        try:
            self.bot.unload_extension('cogs.' + cog)
        except commands.ExtensionError as err:
            return await ctx.send(err)
        await ctx.send(f'{cog} unloaded.')

    @commands.command(hidden=True)
    async def reload(self, ctx, cog: str):
        """
        Reload a cog.

        Required Permissions:
        Bot owner or admin only.

        Command Usage:
        `reload <cog>`
        """
        try:
            self.bot.reload_extension('cogs.' + cog)
        except commands.ExtensionError as err:
            return await ctx.send(err)
        await ctx.send(f'{cog} reloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        Closes the bot.

        Required Permissions:
        Bot owner only.

        Command Usage:
        `shutdown`
        """
        await ctx.send('Bye, bye!')
        await self.bot.session.close()
        await self.bot.close()

    @commands.command(hidden=True)
    async def sudo(self, ctx, who: Union[discord.Member, discord.User], *, command: str):
        """Run a command as another user."""
        msg = copy(ctx.message)
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command(hidden=True)
    async def do(self, ctx, times: int, *, command):
        """Repeats a command a specified number of times."""
        msg = copy(ctx.message)
        msg.content = ctx.prefix + command

        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        for _ in range(times):
            await new_ctx.reinvoke()


def setup(bot):
    bot.add_cog(Admin(bot))
