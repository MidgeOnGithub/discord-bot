import json

from discord.ext import commands

from src.utils import misc
from src.botcredentials import TWITCH_CLIENT_ID


class HTTPForbiddenError(Exception):
    """
    Exception raised if a given response includes a 401 status.
    """
    def __init__(self, message: str = 'Response included 401 status.'):
        super().__init__(message)


class TwitchClientIDError(HTTPForbiddenError):
    """
    Exception if the bot's credential's file provided an invalid ClientID.
    """
    def __init__(self):
        super().__init__('Bad Twitch client ID.')


class Twitch(commands.Cog):
    """Provides simple statistics commands."""

    def __init__(self, bot):
        self.bot = bot
        self.twitch_client_id = {'Client-ID': TWITCH_CLIENT_ID}

    @commands.command()
    async def top_games(self, ctx, amount=10):
        """
        Display the top twitch games sorted by current viewership.

        Command Usage:
        `twitch top_games <1 - 20>`
        """
        amount = 1 if amount < 1 else amount
        amount = 20 if amount > 20 else amount

        url = 'https://api.twitch.tv/helix/games/top'
        payload = await self._fetch_payload(url, twitch_api=True)
        games = [listing['name'] for listing in payload['data'][:amount]]

        games_strings = misc.numbered_strings_from_list(games)
        await ctx.send('Current top {} Twitch games by viewers:\n```'
                       '{}```'.format(amount, '\n'.join(games_strings)))

    @commands.command()
    async def top_streamers(self, ctx, amount=10):
        """
        Display the top twitch streamers sorted by current viewership.

        Command Usage:
        `twitch top`
        `twitch top_streamers <1 - 20>
        """
        amount = 1 if amount < 1 else amount
        amount = 20 if amount > 20 else amount

        url = f'https://api.twitch.tv/helix/streams?first={amount}'
        payload = await self._fetch_payload(url, twitch_api=True)
        streamers = []
        viewer_counts = []
        for listing in payload['data'][:amount]:
            streamers.append(listing['user_name'])
            viewer_counts.append(listing['viewer_count'])

        streamers = misc.numbered_strings_from_list(streamers)
        message_strings = [f'{name} -- {viewers} viewers'
                           for name, viewers in zip(streamers, viewer_counts)]
        await ctx.send('Current top {} Twitch streamers by viewers:\n```'
                       '{}```'.format(amount, '\n'.join(message_strings)))

    async def _fetch_payload(self, url, twitch_api=True):
        """
        Fetches a response from the given URL and formats it to a usable payload.
        """
        if twitch_api:
            async with self.bot.session.get(url, headers=self.twitch_client_id) as response:
                if response.status == 401:
                    raise TwitchClientIDError
                usable_payload = json.loads(await response.text())
        else:
            async with self.bot.session.get(url) as response:
                if response.status == 401:
                    raise HTTPForbiddenError
                usable_payload = await response.text()
        return usable_payload


def setup(bot):
    bot.add_cog(Twitch(bot))
