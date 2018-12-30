import discord
from discord.ext import commands

# In cogs, client events do not need a @client.event decorator
# But commands need @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client

    async def ban_kick(self, ctx, target: discord.User = None,
                       reason=None, ban=False):
        # Set verbs according to which command the user invoked
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # Checks for misuses
        # @ban.error decorator handles cases involving invalid targets
        if target is None:
            await ctx.send(f'Usage: `!{w1} @target`')
            return
        if target == ctx.message.author:
            await ctx.send(f'You cannot {w1} yourself!')
            return
        # Bots shouldn't be banned/kicked by another bot
        if target.bot:
            await ctx.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Check if bot and author have the required guild permissions
        if ban:
            author_perms = ctx.message.author.guild_permissions.ban_members
            bot_perms = ctx.me.guild_permissions.ban_members
        else:
            author_perms = ctx.message.author.guild_permissions.kick_members
            bot_perms = ctx.me.guild_permissions.kick_members
        if not author_perms:
            await ctx.send(f'You do not have permissions to {w1} members.')
            return
        if not bot_perms:
            await ctx.send(f'I do not have permissions to {w1} members.')
            return
        # Check if the user is already banned
        # If so, give reason and exit
        try:
            # Collect a BanEntry tuple for the user, if it exists
            # Index 0 contains username, index 1 contains reason
            # If BanEntry doesn't exist, discord.NotFound error raises
            ban_info = await ctx.guild.get_ban(target)
            # By default, ban audit reason is None
            if ban_info[1]:
                reason = f'Reason: `{ban_info[1]}`.'
            else:
                reason = 'No reason was given.'
            await ctx.send(f'{ban_info[0]} was already banned.\n{reason}')
            return
        except discord.NotFound:
            pass
        # A ban/kick fails if target has a "higher" role than the bot
        try:
            if ban:
                await ctx.guild.ban(target, reason)
            else:
                await ctx.guild.kick(target)
        except discord.Forbidden:
            await ctx.send(f'I cannot {w1} {target} due to their elevated role(s).')
            return
        # Notify both target and channel upon ban/kick completion
        msg1 = f'You have been {w2} from {ctx.guild.name}!'
        await target.send(msg1)
        msg2 = f'{target} was {w2}!'
        await ctx.send(msg2)

    @commands.command()
    async def ban(self, ctx, target: discord.User = None,
                  reason=None):
        # Call ban_kick with ban set to True
        await self.ban_kick(ctx, target, reason, True)

    # Use a local error handler to catch errors in command's invocation
    @ban.error
    async def ban_kick_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f'{error.args[0]}.')
        else:
            print(error)

    @commands.command()
    async def kick(self, ctx, target: discord.User = None,
                   reason=None):
        # Call ban_kick without setting ban to True
        await self.ban_kick(ctx, target, reason)

    # Because @<command>.error handlers are local, kick needs a "dummy"
    @kick.error
    async def kick_handler(self, ctx, error):
        await self.ban_kick_handler(ctx, error)


def setup(client):
    client.add_cog(Moderation(client))
