import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
# Commands need @commands.command() instead of @client.command()

class Live_Role:
    def __init__(self, client):
        self.client = client

        # Game names must be formatted to match exactly the name in Twitch's directory
        self.games_filter = [
            # Import a user-given game filter somehow
            #  Also create helper functions to add and remove games from said filter
            #  If this is quite complex, a separate cog may be needed
        ]

        self.member_exceptions = [
            # Implement a means to "ignore" the game filter list for certain users as desired
        ]

    # Consider moving to commands into "moderation" cog, editing calls within on_member_update here accordingly
    def remove_role(self, member, role, reason=None):
        if role in member.roles:
            member.remove_roles(role, reason)


    # This is the event which will update the 'Live' role based on if a person is streaming an applicable game
    async def on_member_update(self, before, after):
        # First get info for the server's 'Live' role
        #  Currently this is just hardcoded as 'Live' but in the future it should be changeable by settings
        live_role = discord.utils.get(after.server.roles, name = 'Live')
        rem_reason = 'No longer streaming a game from the game filter.'
        # If a user has started or updates their streaming status and is playing a game from the selection, assign the role to them
        if discord.Streaming in after.activities:
            if after.Streaming.details in self.games_filter:
                if live_role not in after.roles:  # Role does not need reassigned if already present
                    await after.add_role(after, live_role)
            else:
                self.remove_role(after, live_role, rem_reason)
        # If a user is not (or no longer) streaming an appropriate game, be sure they don't have the role
        elif discord.Streaming not in after.activities:
            self.remove_role(after, live_role, rem_reason)


def setup(client):
    client.add_cog(Live_Role(client))

