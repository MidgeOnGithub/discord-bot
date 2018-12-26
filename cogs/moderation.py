import discord
from discord.ext import commands

# In cogs, client events do not need any sort of @client.event decorator
#  Additionally, commands require @commands.command() instead of @client.command()

class Moderation:
    def __init__(self, client):
        self.client = client


    async def ban_kick(self, ctx, target:discord.User = None, reason = None, ban = False):
        # Set the action word according to which command the user invoked
        if ban:
            w1, w2 = 'ban', 'banned'
        else:
            w1, w2 = 'kick', 'kicked'
        # Checks for misuses
        #  Note that @ban.error handles cases with an invalid target
        if target == None:
            await ctx.channel.send(f'Usage: `!{w1} @target`')
            return
        if target == ctx.message.author:
            await ctx.channel.send(f'You cannot {w1} yourself!')
            return
        # Bots shouldn't be banned/kicked by a bot
        if target.bot:
            await ctx.channel.send(f'{target} is a bot -- I cannot ban them.')
            return
        # Checks if the bot and the invoker have the required permissions to execute the command
        try:
            if ban:
                commands.bot_has_permissions(ban_members=True)
                print('Bot has permissions')
                commands.has_permissions(ban_members=True)
                print('Message author has permissions')
                await ctx.channel.send(ctx.message.author.guild_permissions)
            else:
                commands.bot_has_permissions(kick_members=True)
                commands.has_permissions(kick_members=True)
        except commands.BotMissingPermissions:
            await ctx.channel.send(f'I don\'t have permission to {w1} people.')
            return
        except commands.MissingPermissions:
            await ctx.channel.send(f'You don\'t have permission to {w1} people.')
            return
        # Check if the user is already banned -- if so, give the reason and exit
        try:
            # Collect a BanEntry tuple for the user, if it exists
            ban_info = await ctx.guild.get_ban(target)
            # By default, when banning, reason is None
            if ban_info[1]:
                reason = f'Reason: `{ban_info[1]}`.'
            else:
                reason = 'No reason was given.'
            await ctx.channel.send(f'{ban_info[0]} was already banned.\n{reason}')
            return
        except discord.NotFound:
            print('User is not already banned')
            pass  # If the user is not on the list, continue
        # A ban/kick will fail if the target has a "higher" role than the bot and/or the bot doesn't have the ban_member permissions
        try:
            if ban:
                await ctx.guild.ban(target)
            else:
                await ctx.guild.kick(target)
        except discord.Forbidden:
            await ctx.channel.send(f'I cannot {w1} {target} because they have more elevated permissions/roles than me.')
            return
        # Notify both target and channel upon ban/kick completion
        msg1 = f'You have been {w2} from {ctx.guild.name}!'
        await target.send(msg1)
        msg2 = f'{target} was {w2}!'
        await ctx.channel.send(msg2)


    @commands.command()
    async def ban(self, ctx, target:discord.User = None, reason = None):
        # Call ban_kick with ban set to True
        await self.ban_kick(ctx, target, reason, True)

    # Using a local error handler allows catching errors in command's invocation
    @ban.error
    async def ban_kick_handler(self, ctx, error):
        print('we\'re here')
        if isinstance(error, commands.BadArgument):
            await ctx.channel.send(f'{error.args[0]}.')
        else:
            print(error)


    @commands.command()
    async def kick(self, ctx, target:discord.User = None, reason = None):
        # Call ban_kick without setting ban to True
        await self.ban_kick(ctx, target, reason)

    # Because @<command>.error handlers are local, need to create a "dummy" version for kick
    @kick.error
    async def kick_handler(self, ctx, error):
        await self.ban_kick_handler(ctx, error)


def setup(client):
    client.add_cog(Moderation(client))

