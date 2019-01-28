import discord
from discord.ext import commands

# In cogs, bot events do not need a @bot.event decorator
# But commands need @commands.command() instead of @bot.command()

class Live:

    def __init__(self, bot):
        self.bot = bot

        self.game_filter = [
            # Game names must match exactly a name in Twitch's directory
            # TODO: Filter should be configurable
            # TODO: Make commands to add, remove, replace filter entries
            # TODO: If this is quite complex, a separate cog may be needed
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
        if discord.Streaming in (before.activities, after.activities):
            await self.live_update(after)

    # Update the 'Live' role according to members' changes in streaming
    async def live_update(self, after: discord.Member):
        # Get server's 'Live' role
        # TODO: 'Live' role name should be configurable
        live_role = discord.utils.get(after.guild.roles, name='Live')
        if (discord.Streaming not in after.activities and
            live_role in after.roles):
            # Remove 'Live' role if they are longer streaming
            return await self.change_role(after, live_role)
        # Assign 'Live' role to a member who starts or updates a stream
        # but only if playing from game_filter or exempt from it
        if discord.Streaming in after.activities:
            if (after not in self.member_blacklist and
                (after in self.member_whitelist or
                self.game_filter is None or
                after.Streaming.details in self.game_filter)):
                return await self.change_role(after, live_role)

        if discord.Streaming in after.activities:
            if (after.Streaming.details in self.game_filter or
                self.game_filter is None):
                # Do not reassign 'Live' role if already present
                if live_role not in after.roles:
                    await self.change_role(after, live_role)
            else:
                await self.change_role(after, live_role)

    # TODO: Maybe make this a command in moderation cog instead (DRY)
    async def change_role(self, member, role, reason=None, remove=False):
        if role in member.roles:
            # TODO: Fix the incorrect condition below
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    print(f'Cannot alter `{role}` due to ' +
                          'elevated permissions.')
            else:
                # No need to add the role if member already has it
                print(f'{member.display_name} already has the ' +
                      f'`{role}` role -- no change.')
        else:
            # TODO: Fix the incorrect condition below
            if remove:
                # No need to remove role if member does not have it
                print(f'{member.display_name} does not have the ' +
                      f'`{role}` role -- no change.')
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f'Cannot alter `{role}` due to ' +
                          'elevated permissions.')


def setup(bot):
    bot.add_cog(Live(bot))
