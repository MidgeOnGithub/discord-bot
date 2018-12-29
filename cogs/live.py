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
            ### Create commands to add, remove, replace filter entries
            ### If this is quite complex, a separate cog may be needed
        ]

        self.member_whitelist = [
            ### Implement a whitelist for members to "ignore" game_filter
            ### Create commands to add, remove, replace whitelist entries
        ]

    # Consider moving to "moderation" cog, editing on_member_update
    def remove_role(self, member, role, reason=None):
        if role in member.roles:
            member.remove_roles(role, reason)

    # Update the 'Live' role if a person is streaming from game_filter
    async def on_member_update(self, before, after):
        # Get server's 'Live' role
        #  Currently hardcoded as 'Live' but should be configurable
        live_role = discord.utils.get(after.guild.roles, name='Live')
        rem_reason = 'No longer streaming a game from the game filter.'
        # Assign 'Live' role to a member who starts or updates a stream
        #  playing from game_filter (or game_filter doesn't exist)
        if discord.Streaming in after.activities:
            if (after.Streaming.details in self.game_filter or
                    self.game_filter == []):
                # Do not reassign 'Live' role if already present
                if live_role not in after.roles:
                    await after.add_role(after, live_role)
            else:
                self.remove_role(after, live_role, rem_reason)
        # Remove 'Live' role if member is no longer streaming
        elif discord.Streaming not in after.activities:
            if live_role in after.roles:
                self.remove_role(after, live_role, rem_reason)


def setup(client):
    client.add_cog(Live(client))
