import json

import discord
from discord.ext import commands

from botcredentials import TWITCH_CLIENT_ID


class TwitchClientIDError(Exception):
    """
    Exception if the bot's credential's file is giving a bad ClientID.
    """
    def __init__(self):
        super().__init__('Bad Twitch client ID.')


class Twitch(commands.Cog):
    """Provides simple statistics commands."""
    def __init__(self, bot):
        self.bot = bot
        self.twitch_client_id = {'Client-ID': TWITCH_CLIENT_ID}

    @commands.command()
    async def top_games(self, ctx):
        """
        Display basic bot information.

        Command Usage:
        `twitch top`
        """
        url = 'https://api.twitch.tv/helix/games/top'
        async with self.bot.session.get(url, headers=self.twitch_client_id) as response:
            if response.status == 401:
                raise TwitchClientIDError
            usable_payload = json.loads(await response.text())
        games = [listing['name'] for listing in usable_payload['data']]
        await ctx.send(f'Current top 10 Twitch games by views:\n```'
                       f'{", ".join(games[:10])}```')


def setup(bot):
    bot.add_cog(Twitch(bot))



