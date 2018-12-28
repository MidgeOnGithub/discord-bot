import discord
from discord.ext import commands

# In cogs, client events do not need a @client.event decorator
# But commands need @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client

    async def ban_kick(self, ctx, target: discord.User = None, reason=None, ban=False):
        # Set the action word according to which command the user invoked
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # Checks for misuses
        # @ban.error decorator handles cases involving invalid targets
        if target == None:
            await ctx.channel.send(f'Usage: `!{w1} @target`')
            return
        if target == ctx.message.author:
            await ctx.channel.send(f'You cannot {w1} yourself!')
            return
        # Bots shouldn't be banned/kicked by another bot
        if target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Check if bot and author have the required guild permissions
        if ban:
            author_perms = ctx.message.author.ban_members
            bot_perms = self.client.user.ban_members
        else:
            author_perms = ctx.message.author.kick_members
            bot_perms = self.client.user.kick_members
        if not author_perms:
            await ctx.channel.send(f'You do not have permissions to {w1} members.')
        if not bot_perms:
            await ctx.channel.send(f'I do not have permissions to {w1} members.')
        # Check if the user is already banned
        # If so, give reason and exit
        try:
            # Collect a BanEntry tuple for the user, if it exists
            # Index 0 contains username, index 1 contains reason
            # If this entry doesn't exist, a discord.NotFound error will raise
            ban_info = await ctx.guild.get_ban(target)
            # By default, ban audit reason is None
            if ban_info[1]:
                reason = f'Reason: `{ban_info[1]}`.'
            else:
                reason = 'No reason was given.'
            await ctx.channel.send(f'{ban_info[0]} was already banned.\n{reason}')
            return
        except discord.NotFound:
            pass
        # A ban/kick will fail if the target has a "higher" role than the bot and/or the bot doesn't have the ban_member permissions
        try:
            if ban:
                await ctx.guild.ban(target)
            else:
                await ctx.guild.kick(target)
        except discord.Forbidden:
            await ctx.channel.send(f'I cannot {w1} {target} due to more elevated permissions/roles.')
            return
        # Notify both target and channel upon ban/kick completion
        msg1 = f'You have been {w2} from {ctx.guild.name}!'
        await target.send(msg1)
        msg2 = f'{target} was {w2}!'
        await ctx.channel.send(msg2)

    @commands.command()
    async def ban(self, ctx, target: discord.User = None, reason=None):
        # Call ban_kick with ban set to True
        await self.ban_kick(ctx, target, reason, True)

    # Use a local error handler to catch errors in command's invocation
    @ban.error
    async def ban_kick_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.channel.send(f'{error.args[0]}.')
        else:
            print(error)

    @commands.command()
    async def kick(self, ctx, target: discord.User = None, reason=None):
        # Call ban_kick without setting ban to True
        await self.ban_kick(ctx, target, reason)

    # Because @<command>.error handlers are local, must have a "dummy" version for kick
    @kick.error
    async def kick_handler(self, ctx, error):
        await self.ban_kick_handler(ctx, error)


def setup(client):
    client.add_cog(Moderation(client))

