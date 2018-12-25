import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
#  Additionally, commands require @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ban(self, ctx, target:discord.Member = None, alert = True):
        # This section checks for misuses
        if target == ctx.message.author:
            await ctx.channel.send('You cannot ban yourself!')
            return
        elif target == None:
            await ctx.channel.send('Who do you want to ban?')
            return
        # Bots can't be banned by a bot nor messaged
        elif target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Ban them, send a message to them regarding the ban
        msg = f'You have been banned from {ctx.guild.name}!'
        await target.send(msg)
        await ctx.guild.ban(target)
        # By default, alert the channel of the ban, this can be overridden on command execution
        if alert:
            await ctx.channel.send(f'{target} is banned!')
        # Delete the msg giving the ban command
        await ctx.message.delete()


def setup(client):
    client.add_cog(Moderation(client))

