from glob import glob
from os import path

import discord
from discord.ext import commands


class Owner(commands.Cog):
    """Owner-only actions for core bot functionalities and features."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def load(self, ctx, cog: str):
        """
        Load a cog.

        Command Usage:
        `load moderation`
        """
        try:
            self.bot.load_extension('cogs.' + cog)
            await ctx.send(f'{cog} loaded.')
        except (discord.ClientException, ImportError) as err:
            print(f'{cog} not loaded. [{err}]')
            await ctx.send(f'{cog} was not loaded. Check it exists and has a proper `setup` function.')

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str):
        """
        Unload a cog.

        Command Usage:
        `unload stats`
        """
        try:
            self.bot.unload_extension('cogs.' + cog)
            await ctx.send(f'{cog} unloaded.')
        except Exception as e:
            print(f'{cog} not unloaded. [{e}]')
            await ctx.send(f'{cog} was not unloaded.')

    @commands.command(hidden=True)
    async def reload(self, ctx, cog: str):
        """
        Reload a cog.

        Command Usage:
        `reload live`
        """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception:
            return await ctx.send(f'{cog} not reloaded.')
        else:
            return await ctx.send(f'{cog} reloaded.')


    def _cog_file_available(self, cog):
        """Determines if a cog file exists within the program's known directories."""
        return cog in self._cog_files()

    @staticmethod
    def _cog_files():
        """Returns a list of cog files within the program's known directories."""
        cogs = [path.basename(f) for f in glob("cogs/*.py")]
        return ["cogs." + path.splitext(f)[0] for f in cogs]

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
        try:
            await discord.Client.close(self.bot)
        except commands.NotOwner:
            ctx.send(f'Only the bot owner may issue this command.')



def setup(bot):
    bot.add_cog(Owner(bot))
