import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
#  Additionally, commands require @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client


    async def ban_kick(self, ctx, target:discord.Member = None, reason = None, ban = False):
        # Set the action word according to which command the user invoked
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # This section checks for misuses
        if target == None:
            await ctx.channel.send(f'Usage: `!{w1} @target`')
            return
        if target == ctx.message.author:
            await ctx.channel.send(f'You cannot {w1} yourself!')
            return
        # Bots shouldn't be banned/kicked nor messaged by a bot 
        if target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Check if the user is already banned -- if so, give the reason and exit
        try:
            ban_info = await ctx.guild.get_ban(target)
            reason = 'No reason was given.'
            if ban_info[1]:
                reason = f'\nReason: `{ban_info[1]}`.'
            await ctx.channel.send(f'{ban_info[0]} was already banned.{reason}')
        except:
            pass
        # A ban/kick will fail if the target has a "higher" role than the bot and/or the bot doesn't have the ban_member permissions
        try:
            if ban:
                await ctx.guild.ban(target)
            else:
                await ctx.guild.kick(target)
        except:
            await ctx.channel.send(f'I do not have the required permissions to {w1} {target}.')
            return
        # Notify the target and the guild channel upon ban/kick completion
        msg1, msg2 = f'You have been {w2} from {ctx.guild.name}!', f'{target} was {w2}!'
        await target.send(msg1)
        await ctx.channel.send(msg2)


    @commands.command()
    async def ban(self, ctx, target:discord.Member = None, reason=None):
        # Call ban_kick with ban set to True
        await self.ban_kick(ctx, target, reason, True)


    @commands.command()
    async def kick(self, ctx, target:discord.Member = None, reason = None):
        # Call ban_kick without setting ban to True
        await self.ban_kick(ctx, target, reason)
        

def setup(client):
    client.add_cog(Moderation(client))

