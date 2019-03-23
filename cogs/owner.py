import discord
from discord.ext import commands


class Owner(commands.Cog):
    """Owner-only actions for core bot functionalities and features."""

    def __init__(self, bot):
        self.bot = bot
        self.settings_cog = self.bot.get_cog('Settings')

    @commands.command(hidden=True)
    async def cogs(self, ctx):
        """
        Retrieve the list of loaded cogs.

        Command Usage:
        `cogs`
        """
        cogs = [cog[5:] for cog in self.bot.extensions.keys()]
        await ctx.send(f'Loaded cogs:\n```{cogs}```')

    @commands.command(hidden=True)
    async def load(self, ctx, cog: str):
        """
        Load a cog.

        Command Usage:
        `load <cog>`
        """
        try:
            self.bot.load_extension('cogs.' + cog)
        except commands.ExtensionError as err:
            return await ctx.send(err)
        await ctx.send(f'{cog} loaded.')

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str):
        """
        Unload a cog, unless it is a core cog.

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
        await discord.Client.close(self.bot)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def set_admin_role(self, ctx, target: discord.User = None):
        pass



def setup(bot):
    bot.add_cog(Owner(bot))
