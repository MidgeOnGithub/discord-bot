from datetime import datetime

import discord
from discord.ext import commands

# In cogs, client events do not need a @client.event decorator
# But commands need @commands.command() instead of @client.command()

class BotManagement:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def load(self, ctx, ext):
        try:
            self.client.load_extension(ext)
            print(f'Loaded {ext}')
            await ctx.channel.send(f'{ext} loaded.')
        except Exception as err:
            print(f'{ext} not loaded. [{err}]')
            await ctx.channel.send(f'{ext} was not loaded.')

    @commands.command()
    async def unload(self, ctx, ext):
        try:
            self.client.unload_extension(ext)
            print(f'Unloaded {ext}')
            await ctx.channel.send(f'{ext} unloaded.')
        except Exception as err:
            print(f'{ext} not unloaded. [{err}]')
            await ctx.channel.send(f'{ext} was not unloaded.')

    @commands.command()
    async def ping(self, ctx):
        # Tests the bot's ping
        ping = round(self.client.latency * 1000)
        await ctx.channel.send(f'My ping is {ping} ms')

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days < 1:
            d_msg = ''
        else:
            d_msg = f'{days} days, '
        await ctx.send(f'Uptime: {d_msg}{hours} hours, {minutes} minutes, and {seconds} seconds')


def setup(client):
    client.add_cog(BotManagement(client))
