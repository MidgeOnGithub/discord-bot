from datetime import datetime

import discord
from discord.ext import commands


class Stats(commands.Cog):
    """Provides simple statistics commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        await ctx.send(f'A simple python Discord bot scripted by Midge.\n'
                       f'https://github.com/MidgeOnGithub/discord-bot')

    @commands.command()
    async def uptime(self, ctx):
        """
        Returns the bot's uptime.

        Command Usage:
        `uptime`
        """
        # From https://github.com/Rapptz/RoboDanny
        delta_uptime = datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        d_msg = '' if (days < 1) else f'{days} days'
        await ctx.send(f'Uptime: {d_msg}{hours} hours, {minutes} minutes, {seconds} seconds.')

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, target: discord.Member = None):
        """
        Gets and returns information about a guild member,
        either the invoker or a specified target.

        Command usage:
        `user <target_with#discriminator>`
        """
        # Determine who is the target, set pronouns accordingly
        # If no target is specified, invoking member is target
        if target is None:
            target = ctx.message.author
            p1, p2 = 'Your', 'You'
        elif target.bot:
            p1, p2 = 'Its', 'It'
        else:
            p1, p2 = 'Their', 'They'
        # Determine certain properties and text regarding the target
        nick = target.display_name
        username = f'{target.name}#{target.discriminator}'
        join_time = target.joined_at
        # Say a member's top role if they have one beyond @everyone
        if len(target.roles) != 1:
            role = target.top_role
            r_msg = f'{p1} top role is {role}.'
        else:
            # Using this message prevents pinging @everyone
            r_msg = f'{p2} has no special roles.'
        # Point out if the member is a bot
        if target.bot:
            bot_msg = f'{nick} is a bot.'
        else:
            bot_msg = ''
        # Send the message
        return await ctx.send(
            f'Full username: {username}.\n'
            f'{p2} joined at {join_time}.\n'
            f'{r_msg} {bot_msg}'
        )


def setup(bot):
    bot.add_cog(Stats(bot))

