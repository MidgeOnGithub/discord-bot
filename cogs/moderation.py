import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
#  Additionally, commands require @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client


    #Combine the kick and ban commands into one per DRY standard
    @commands.command()
    async def ban(self, ctx, target:discord.Member = None, reason=None):
        # This section checks for misuses
        if target == ctx.message.author:
            await ctx.channel.send('You cannot ban yourself!')
            return
        elif target == None:
            await ctx.channel.send('Who do you want to ban?')
            return
        # Bots can't be banned/kicked nor messaged by a bot 
        elif target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Ban them, send a message to them regarding the ban
        msg = f'You have been banned from {ctx.guild.name}!'
        await target.send(msg)
        await ctx.guild.ban(target)
        # Alert the channel of the ban's completion
        await ctx.channel.send(f'{target} is banned!')
        # Delete the msg invoking the ban command
        await ctx.message.delete()


    @commands.command()
    async def kick(self, ctx, target:discord.Member = None, reason=None):
        # This section checks for misuses
        if target == ctx.message.author:
            await ctx.channel.send('You cannot kick yourself!')
            return
        elif target == None:
            await ctx.channel.send('Who do you want to kick?')
            return
        # Bots can't be banned/kicked nor messaged by a bot 
        elif target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot kick them.')
            return
        # Ban them, send a message to them regarding the ban/kick
        msg = f'You have been kicked from {ctx.guild.name}!'
        await target.send(msg)
        await ctx.guild.kick(target)
        # Alert the channel of the ban/kick completion
        await ctx.channel.send(f'{target} was kicked!')
        # Delete the msg invoking the ban/kick command
        await ctx.message.delete()


def setup(client):
    client.add_cog(Moderation(client))

