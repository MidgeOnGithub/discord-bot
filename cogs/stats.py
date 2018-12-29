import discord
from discord.ext import commands

# In cogs, client events do not need a @client.event decorator
# But commands need @commands.command() instead of @client.command()

class Stats:
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def user(self, ctx, target: discord.Member = None):
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
        # Point out a member's top role if they have one beyond @everyone
        if len(target.roles) != 1:
            role = target.top_role
            r_msg = f'{p1} top role is {role}.'
        else:
            # Using this message prevents pinging @everyone
            r_msg = f'{nick} has no special roles.'
        # Point out if the member is a bot
        if target.bot:
            bot_msg = f'\n{nick} is a bot.'
        else:
            bot_msg = ''
        # Send the message
        await ctx.channel.send(f'{nick}\'s full username is {username}.\n{p2} joined at {join_time}.\n{r_msg}{bot_msg}')


def setup(client):
    client.add_cog(Stats(client))

