import discord
from discord.ext import commands

# In cogs, bot events do not need a @bot.event decorator
# But commands need @commands.command() instead of @bot.command()

class Live:
    """Gives live roles to eligble members playing eligible games."""
    def __init__(self, bot):
        self.bot = bot

        self.game_filter = [
            # Game names must match a name in Twitch's directory
            # TODO: Filter should be configurable
            # TODO: Make commands to add and remove filter entries
            # TODO: If this is complex, separate cog may be needed
        ]

        self.member_blacklist = [
            # TODO: Add whitelist for members who never want the role
            # TODO: Commands to add and remove blacklist entries
        ]

        self.member_whitelist = [
            # TODO: Add whitelist for members who bypass game_filter
            # TODO: Commands to add and remove whitelist entries
        ]

    async def on_member_update(self, before, after):
        # Ignore if the member is in the blacklist
        if before not in self.member_blacklist:
            if discord.Streaming in (before.activities, after.activities):
                return await self.live_update(after)

    async def live_update(self, after: discord.Member):
        """
        Updates guild's live role according to members'
        streaming status.
        """
        # Get server's 'Live' role
        # TODO: 'Live' role name should be configurable
        live_role = discord.utils.get(after.guild.roles, name='Live')
        live = discord.Streaming in after.activities
        has_role = live_role in after.roles
        # Remove the role if they are no longer streaming
        if not live and has_role:
            return await self.change_role(after, live_role, True)
        # Assign the role to a member who starts or updates a stream
        # but only if playing from game filter (or exempt from it)
        eligible = (after in self.member_whitelist or
                    self.game_filter is None or
                    after.Streaming.details in self.game_filter)
        if live and eligible and not has_role:
            return await self.change_role(after, live_role)

    # TODO: Maybe make this a command in moderation cog instead (DRY)
    async def change_role(self, member, role,
                          remove=False, reason=None):
        """Adds or removes a role from a guild member."""
        if role in member.roles:
            # TODO: Fix the incorrect condition below
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to ' +
                          'elevated permissions.')
            else:
                # No need to add the role if member already has it
                print(f'{member.display_name} already has the ' +
                      f'`{role}` role -- no change.')
        else:
            if remove:
                # No need to remove role if member does not have it
                print(f'{member.display_name} does not have the ' +
                      f'`{role}` role -- no change.')
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to ' +
                          'elevated permissions.')


def setup(bot):
    bot.add_cog(Live(bot))
