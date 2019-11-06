from datetime import datetime

import discord
from discord.ext import commands


class Stats(commands.Cog):
    """Provides simple statistics commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias=('bot', 'bot_info'))
    async def info(self, ctx):
        """
        Display basic bot information.

        Command Usage:
        `info`
        `bot`
        `bot_info`
        """
        await ctx.send(f'A simple python Discord bot scripted by Midge.\n'
                       f'<https://github.com/MidgeOnGithub/discord-bot>')

    @commands.command()
    async def ping(self, ctx):
        """
        "Pong!" + latency.

        Command Usage:
        `ping`
        """
        ping = round(self.bot.latency * 1000)
        await ctx.channel.send(f'Pong! My ping is {ping} ms.')

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
        days_msg = '' if (days < 1) else f'{days} days'
        await ctx.send(f'Uptime: {days_msg}{hours} hours, {minutes} minutes, {seconds} seconds.')

    @commands.command()
    @commands.guild_only()
    async def user_info(self, ctx, *, target: discord.Member = None):
        """
        Gets and returns information about a guild member.
        If no target is specified, the target becomes the invoker.

        Command Usage:
        `user_info`
        `user_info <target_with#discriminator>`
        """
        # Set words according to who is the target.
        if target is None:
            target = ctx.message.author
            p1, p2, p3 = 'Your', 'You', 'have'
        elif target.bot:
            p1, p2, p3 = 'Its', 'It', 'has'
        else:
            p1, p2, p3 = 'Their', 'They', 'have'
        # Determine certain properties and text regarding the target
        nick = target.display_name
        username = f'{target.name}#{target.discriminator}'
        join_time = target.joined_at
        # Say a member's top role if they have one beyond @everyone
        if len(target.roles) != 1:
            role = target.top_role
            r_msg = f'{p1} top role is {role}.'
        else:
            r_msg = f'{p2} {p3} no special roles.'
        # Point out if the member is a bot
        bot_msg = f'{nick} is a bot' if target.bot else ''
        # Send the message
        await ctx.send(f'Full username: {username}.\n'
                       f'{p2} joined at {join_time}.\n'
                       f'{r_msg} {bot_msg}')


def setup(bot):
    bot.add_cog(Stats(bot))

