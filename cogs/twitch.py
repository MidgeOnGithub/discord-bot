import json

from discord.ext import commands

import utils.misc
from botcredentials import TWITCH_CLIENT_ID


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
        `twitch top`
        """
        if amount < 1:
            amount = 1
        elif amount > 20:
            amount = 20
        url = 'https://api.twitch.tv/helix/games/top'
        payload = await self._fetch_payload(url, twitch_api=True)
        games = [listing['name'] for listing in payload['data']]
        games_strings = utils.misc.numbered_strings_from_list(games[:amount])
        await ctx.send('Current top {} Twitch games by viewers:\n```'
                       '{}```'.format(amount, '\n'.join(games_strings)))

    @commands.command()
    async def top_streamers(self, ctx, amount=10):
        """
        Display the top twitch streamers sorted by current viewership.

        Command Usage:
        `twitch top`
        `twitch top <1 - 20>
        """
        if amount < 1:
            amount = 1
        elif amount > 20:
            amount = 20
        url = f'https://api.twitch.tv/helix/streams?first={amount}'
        payload = await self._fetch_payload(url, twitch_api=True)
        # TODO: Condense streamers and viewer_counts to a tuple, so as to only 
        #  iterate through the payload once -- change other code as needed
        streamers = [listing['user_name'] for listing in payload['data'][:amount]]
        viewer_counts = [listing['viewer_count'] for listing in payload['data'][:amount]]
        streamers_strings = utils.misc.numbered_strings_from_list(streamers)
        message_strings = [f'{old_string} -- {viewer_count} viewers'
                           for old_string, viewer_count in zip(streamers_strings, viewer_counts)]
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
