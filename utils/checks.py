import discord
from discord.ext import commands


async def is_admin_or_owner(ctx: commands.context):
    """
    A check that allows only the bot owner or, if applicable, a guild admin to invoke commands.
    """
    author = ctx.author
    # First check if the invoker is the bot owner
    if await ctx.bot.is_owner(author):
        return True
    # If not the bot owner, an invoker may not invoke in a DM
    if not ctx.guild:
        return False
    # Then the slower check
    return await discord.utils.get(author.roles, name=ctx.bot.settings.admin_role)


async def invoked_in_channel(ctx: commands.context, channel_id: int):
    """
    A check that only allows for a command to be invoked in the channel passed to the command.
    """
    return ctx.channel.id == channel_id
