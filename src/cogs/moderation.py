import discord
from discord.ext import commands

from src.utils import checks, misc


class Moderation(commands.Cog):
    """Provides Discord moderation commands for guild mods/admins."""
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return checks.is_mod()

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    async def banned(self, ctx):
        """
        Provides a list of users banned from the guild.
        """
        banned_members = await ctx.guild.bans()
        if banned_members:
            listed_names = misc.numbered_strings_from_list([ban[1] for ban in banned_members])
            msg = '\n'.join(listed_names)
        else:
            msg = 'No users are banned from this guild.'
        await ctx.send(f'List of guild-banned users:\n'
                       f'```{msg}```')

    @commands.command()
    @commands.bot_has_permissions(ban_members=True)
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
        await self._ban_kick(ctx, target, reason, ban=True)

    @commands.command()
    @commands.bot_has_permissions(kick_members=True)
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
        await self._ban_kick(ctx, target, reason, ban=False)

    @staticmethod
    async def _ban_kick(ctx, target: discord.User,
                        reason=None, ban=False):
        """
        Kicks or bans members with respect to `ban`
        """
        # Set verbs appropriately
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # Check for misuses beyond what the default handler and permissions checks catch
        if target == ctx.message.author:
            return await ctx.send(f'You cannot {w1} yourself!')
        elif target.bot:
            return await ctx.send(f'{target} is a bot -- I cannot ban them.')
        elif target == ctx.me:
            # TODO: Make a `leave` command that removes the bot from the guild
            return await ctx.send(f'Nice try... But if you are a guild admin '
                                  f'and want me to leave, use the `leave` command.')
        # Check if the user is already banned; if so, give reason, exit
        try:
            # Collect a BanEntry tuple for the user, if it exists,
            # index 0 contains username, index 1 contains reason
            # If BanEntry doesn't exist, discord.NotFound error raises
            ban_info = await ctx.guild.fetch_ban(target)
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
            return await ctx.send(f'I cannot {w1} {target} due to the role hierarchy.')
        # Notify both target and channel upon ban/kick completion
        try:
            await ctx.message.add_reaction('👍')
        except discord.Forbidden:
            await ctx.send(f'{target} was {w2}.')

    @checks.is_admin()
    @commands.command()
    async def leave(self, ctx):
        ctx.guild.leave()

    @commands.command(aliases=['clear'])
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """
        Purge an amount of messages from the channel.

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

    @staticmethod
    async def _change_role(member: discord.Member, role: discord.Role,
                           remove=False, reason=None):
        """
        Adds or removes a role from a guild member.
        """
        if role in member.roles:
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to the role hierarchy.')
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
                    print(f'Cannot alter the `{role}` role due to the role hierarchy.')


def setup(bot):
    bot.add_cog(Moderation(bot))
