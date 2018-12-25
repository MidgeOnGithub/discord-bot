import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
#  Additionally, commands require @commands.command() instead of @client.command()

class Bot_Management:
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
        await ctx.channel.send(f'My ping is {ping}ms')


def setup(client):
    client.add_cog(Bot_Management(client))

