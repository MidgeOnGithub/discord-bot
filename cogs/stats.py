import discord
from discord.ext import commands

# In cogs, bot events do not need a @bot.event decorator
# But commands need @commands.command() instead of @bot.command()

class Stats:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, target: discord.Member = None):
        """
        Gets and returns information about a guild member,
        either the invoker or a specified target.
        
        Command usage:
        `user <targetwith#discriminator>`
        """
        # Determine who is the target, set pronouns accordingly
        # If no target is specified, invoking member is target
        if target is None:
            target = ctx.message.author
            p1, p2 = 'Your', 'You'
        elif target.bot:  # Assume command won't be invoked by a bot
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
            r_msg = f'{nick} has no special roles.'
        # Point out if the member is a bot
        if target.bot:
            bot_msg = f'{nick} is a bot.'
        else:
            bot_msg = ''
        # Send the message
        await ctx.send(
            f'{nick}\'s full username is {username}.'
            f'{p2} joined at {join_time}.'
            f'{r_msg}'
            f'{bot_msg}'
        )


def setup(bot):
    bot.add_cog(Stats(bot))

