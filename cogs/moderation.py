import discord
from discord.ext import commands

# In cogs, bot events do not need a @bot.event decorator
# But commands need @commands.command() instead of @bot.command()

class Moderation:
    """Provides Discord moderation commands for guild mods/admins."""
    def __init__(self, bot):
        self.bot = bot

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
            return await ctx.send(f'Usage: `!{w1} @target`')
        elif target == ctx.message.author:
            return await ctx.send(f'You cannot {w1} yourself!')
        # Bots shouldn't be banned/kicked by another bot
        elif target.bot:
            return await ctx.send(f'{target} is a bot ' +
                                  '-- I cannot ban them.')
        # Check if bot and author have the required guild permissions
        if ban:
            author_perms = (ctx.message.author.
                            guild_permissions.ban_members)
            bot_perms = ctx.me.guild_permissions.ban_members
        else:
            author_perms = (ctx.message.author.
                            guild_permissions.kick_members)
            bot_perms = ctx.me.guild_permissions.kick_members
        if not author_perms:
            return await ctx.send(f'You do not have permissions ' +
                                  f'to {w1} members.')
        if not bot_perms:
            return await ctx.send(f'I do not have permissions to ' +
                                  f'{w1} members.')
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
            return await ctx.send(f'{ban_info[0]} was already banned.',
                                  f'{reason}')
        except discord.NotFound:
            pass
        # A ban/kick fails if target has a "higher" role than the bot
        try:
            if ban:
                await ctx.guild.ban(target, reason)
            else:
                await ctx.guild.kick(target)
        except discord.Forbidden:
            return await ctx.send(f'I cannot {w1} {target} ' +
                                  'due to their elevated role(s).')
        # Notify both target and channel upon ban/kick completion
        try:
            await ctx.message.add_reaction('👍')
        except discord.Forbidden:
            await ctx.send(f'{target} was {w2}.')
        return

    @commands.command()
    async def ban(self, ctx, target: discord.User = None,
                  reason: str = None):
        """
        Command to ban a user from a guild in which the command is sent.

        Required Permissions:
        `Ban Members`

        Optional Permissions:
        `Add Reactions`

        Command Usage:
        `ban <user#0000> <OPTIONAL: ban reason to log in guild audit>`
        """
        # Call ban_kick with ban set to True
        await self.ban_kick(ctx, target, reason, True)
        try:
            await ctx.message.add_reaction('👍')
        except discord.Forbidden:
            await ctx.send(f'{target} was banned.')
        return

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
        """
        Command to kick a user from a guild in which the command is sent.
        This removes them but does not prevent re-entry.

        Required Permissions:
        `Kick Members`

        Optional Permissions:
        `Add Reactions`

        Command Usage:
        `kick <user#0000>`
        """
        await self.ban_kick(ctx, target, reason)
        try:
            await ctx.message.add_reaction('👍')
        except discord.Forbidden:
            await ctx.send(f'{target} was kicked.')
        return

    # Because @<command>.error handlers are local, kick needs a "dummy"
    @kick.error
    async def kick_handler(self, ctx, error):
        await self.ban_kick_handler(ctx, error)

    # Clear a given amount of messages from channel
    @commands.command(aliases=['purge'])
    async def clear(self, ctx, amount: int):
        """
        Command to clear/purge an amount of messages from the channel.
        This removes them but does not prevent re-entry.

        Required Permissions:
        `Manage Messages`

        Command Usage:
        `clear <amount of messages>`
        `purge <amount of messages>`
        """
        # TODO: Handle `MissingRequiredArgument`
        amount = int(amount)
        # Check that the user entered an amount > 0
        if amount < 1:
            return await ctx.send('Invalid `amount` argument.')

        # Increment amount to delete the invoking message as well
        amount += 1
        # Check invoker and bot permissions before trying to execute
        author_perms = ctx.message.author.guild_permissions.manage_messages
        bot_perms = ctx.me.guild_permissions.manage_messages
        if not author_perms:
            return await ctx.send('You need the `Manage Messages` ' +
                                  'permission in this channel.')
        if not bot_perms:
            return await ctx.send('I need the `Manage Messages` ' +
                                  'permission in this channel.')
        # Delete the messages
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Moderation(bot))
