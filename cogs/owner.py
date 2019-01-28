from datetime import datetime
from glob import glob
from os import path

import discord
from discord.ext import commands

# In cogs, bot events do not need a @bot.event decorator
# But commands need @commands.command() instead of @bot.command()

class Owner:
    """Owner-only actions for core bot functionatities and features."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, cog):
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

    @commands.command()
    async def unload(self, ctx, cog):
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

    @commands.command()
    async def uptime(self, ctx):
        """
        Returns the bot's uptime.

        Command Usage:
        `uptime`
        """
        # From https://github.com/Rapptz/RoboDanny
        delta_uptime = datetime.datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        d_msg = '' if (days < 1) else f'{days} days'
        await ctx.send(f'Uptime: {d_msg}{hours} hours, {minutes} minutes, {seconds} seconds.')

    def _cog_file_available(self, cog):
        """Determines if a cog file exists within the program's known directories."""
        return cog in self._cog_files()

    def _cog_files(self):
        """Returns a list of cog files within the program's known directories."""
        cogs = [path.basename(f) for f in glob("cogs/*.py")]
        return ["cogs." + path.splitext(f)[0] for f in cogs]

def setup(bot):
    bot.add_cog(Owner(bot))
