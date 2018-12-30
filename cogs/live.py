import discord
from discord.ext import commands

# In cogs, client events do not need a @client.event decorator
# But commands need @commands.command() instead of @client.command()

class Live:
    def __init__(self, client):
        self.client = client

        self.game_filter = [
            # Game names must match exactly a name in Twitch's directory
            ### Filter should be configurable
            ### Make commands to add, remove, replace filter entries
            ### If this is quite complex, a separate cog may be needed
        ]

        self.member_whitelist = [
            ### Implement whitelist for members to "ignore" game_filter
            ### Make commands to add, remove, replace whitelist entries
        ]

    async def on_member_update(self, before, after):
        if discord.Streaming in (before.activities, after.activities):
            await self.live_update(after)

    # Update the 'Live' role according to members' changes in streaming
    async def live_update(self, after: discord.Member):
        # Get server's 'Live' role
        ## Hardcoded as 'Live' but should be configurable
        live_role = discord.utils.get(after.guild.roles, name='Live')
        rem_reason = 'No longer streaming a game from the game filter.'
        # Assign 'Live' role to a member who starts or updates a stream
        # Only if playing from game_filter (or game_filter is empty)
        if discord.Streaming in after.activities:
            if (after.Streaming.details in self.game_filter or
                    self.game_filter == []):
                # Do not reassign 'Live' role if already present
                if live_role not in after.roles:
                    await self.change_role(after, live_role)
            else:
                await self.change_role(after, live_role, rem_reason, remove=True)
        # Remove 'Live' role if member is no longer streaming
        elif discord.Streaming not in after.activities:
            if live_role in after.roles:
                await self.change_role(after, live_role, rem_reason, remove=True)

    ## Maybe make this a command in moderation cog instead (DRY)
    async def change_role(self, member, role, reason=None, remove=False):
        if role in member.roles:
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    print(f'Cannot alter {role} due to elevated permissions.')
            else:
                # No need to add the role if member already has it
                print(f'{member} already has {role} -- no change.')
        else:
            if remove:
                # No need to remove role if member does not have it
                print(f'{member.displayname} does not have {role} -- no change.')
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f'Cannot alter {role} due to elevated permissions.')


def setup(client):
    client.add_cog(Live(client))
