import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Provides Discord moderation commands for guild mods/admins."""
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def ban_kick(ctx, target: discord.User,
                       reason=None, ban=False):
        """Kicks or bans members according to the invoked command."""
        # Set verbs appropriately
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # Check if bot and author have the required guild permissions
        if ban:
            author_perms = ctx.message.author.guild_permissions.ban_members
            bot_perms = ctx.me.guild_permissions.ban_members
        else:
            author_perms = ctx.message.author.guild_permissions.kick_members
            bot_perms = ctx.me.guild_permissions.kick_members
        if not author_perms:
            return await ctx.send(f'You do not have permissions to {w1} members.')
        elif not bot_perms:
            return await ctx.send(f'I do not have permissions to {w1} members.')
        # Checks for misuses beyond what handlers and permissions checks catch
        if target is None:
            return await ctx.send(f'Usage: `!{w1} @target`')
        elif target == ctx.message.author:
            return await ctx.send(f'You cannot {w1} yourself!')
        elif target.bot:
            return await ctx.send(f'{target} is a bot -- I cannot ban them.')
        # Check if the user is already banned; if so, give reason, exit
        try:
            # Collect a BanEntry tuple for the user, if it exists,
            # index 0 contains username, index 1 contains reason
            # If BanEntry doesn't exist, discord.NotFound error raises
            ban_info = await ctx.guild.get_ban(target)
            # By default, ban audit reason is None
            if ban_info[1]:
                reason = f'Reason: `{ban_info[1]}`.'
            else:
                reason = 'No reason was given.'
            return await ctx.send(f'{ban_info[0]} was already banned. {reason}')
        except discord.NotFound:
            pass
        # A ban/kick fails if target has a "higher" role than the bot
        try:
            if ban:
                await ctx.guild.ban(target, reason)
            else:
                await ctx.guild.kick(target)
        except discord.Forbidden:
            return await ctx.send(f'I cannot {w1} {target} due to their elevated role(s).')
        # Notify both target and channel upon ban/kick completion
        try:
            await ctx.message.add_reaction('👍')
        except discord.Forbidden:
            await ctx.send(f'{target} was {w2}.')
        return

    @commands.command()
    async def ban(self, ctx, target: discord.User, reason: str = None):
        """
        Ban a user from a guild in which the command is sent.

        Required Permissions:
        `Ban Members`

        Optional Permissions:
        `Add Reactions`

        Command Usage:
        `ban <user#0000> <OPTIONAL: ban reason to log in guild audit>`
        """
        await self.ban_kick(ctx, target, reason, ban=True)

    @commands.command()
    async def kick(self, ctx, target: discord.User, reason=None):
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

    # Clear a given amount of messages from channel
    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amount: int):
        """
        Purge an amount of messages from the channel.
        This removes them but does not prevent re-entry.

        Required Permissions:
        `Manage Messages`

        Command Usages:
        `clear <amount of messages>`
        `purge <amount of messages>`
        """
        # Check the user entered an amount > 0
        if amount < 1:
            return await ctx.send('Invalid `amount` argument.')
        # Increment amount to delete the invoking message as well
        amount += 1
        # Check invoker and bot permissions before trying to execute
        author_perms = ctx.message.author.guild_permissions.manage_messages
        bot_perms = ctx.me.guild_permissions.manage_messages
        if not author_perms:
            return await ctx.send('You need the `Manage Messages` permission in this channel.')
        if not bot_perms:
            return await ctx.send('I need the `Manage Messages` permission in this channel.')
        # Delete the messages
        await ctx.channel.purge(limit=amount)

    # TODO: Finish up the role command(s)
    @commands.command()
    async def role(self, ctx, target: discord.User = None):
        pass

    @staticmethod
    async def change_role(member: discord.Member, role,
                          remove=False, reason=None):
        """Adds or removes a role from a guild member."""
        if role in member.roles:
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to elevated permissions.')
            else:
                # No need to add the role if member already has it
                print(f'{member.display_name} already has the `{role}` role -- no change.')
        else:
            if remove:
                # No need to remove role if member does not have it
                print(f'{member.display_name} does not have the `{role}` role -- no change.')
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to elevated permissions.')


def setup(bot):
    bot.add_cog(Moderation(bot))
