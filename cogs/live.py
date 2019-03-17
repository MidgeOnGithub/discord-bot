import discord
from discord.ext import commands


class Live(commands.Cog):
    """Gives live roles to eligible members playing eligible games."""
    def __init__(self, bot):
        self.bot = bot
        self.game_filter = [
            # Game names must exactly match the name as shown on Twitch
        ]
        self.member_blacklist = []
        self.member_whitelist = []

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Ignore if the member is in the blacklist
        if before not in self.member_blacklist:
            if discord.Streaming in (before.activities, after.activities):
                return await self.live_update(after)

    # TODO: Make this a command in moderation cog instead (DRY)
    async def change_role(self, member, role,
                          remove=False, reason=None):
        """Adds or removes a role from a guild member."""
        if role in member.roles:
            # TODO: Fix the incorrect condition below
            if remove:
                try:
                    await member.remove_roles(role, reason)
                except discord.Forbidden:
                    ctx,send(f'Cannot alter the `{role}` role due to elevated permissions.')
            else:
                # No need to add the role if member already has it
                print(f'{member.display_name} already has the `{role}` role -- no change.')
        else:
            if remove:
                # No need to remove role if member does not have it
                print(f'{member.display_name} does not have the `{role}` role -- no change.')
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f'Cannot alter the `{role}` role due to elevated permissions.')

    # TODO: Per-guild role names
    @staticmethod
    def get_live_role_name(self):
        """Get the live role's name."""
        role = 'Live'
        return role

    async def live_update(self, after: discord.Member):
        """
        Updates guild's live role according to members'
        streaming status.
        """
        # Get server's 'Live' role
        # TODO: 'Live' role name should be configurable
        live_role = discord.utils.get(after.guild.roles,
                                      name=self.get_live_role_name(self))
        live = discord.Streaming in after.activities
        has_role = live_role in after.roles
        # Remove the role if they are no longer streaming
        if not live and has_role:
            return await self.change_role(after, live_role, True)
        # Assign the role to a member who starts or updates a stream
        # but only if playing from game filter (or exempt from it)
        eligible = (after in self.member_whitelist or
                    self.game_filter is None or
                    after.Streaming.details in self.game_filter)
        if live and eligible and not has_role:
            return await self.change_role(after, live_role)

    @commands.group(name='live', invoke_without_command=True)
    async def live(self, ctx):
        await ctx.send(f'Live role command information'
                       f'Commands: `game`, `whitelist`, `blacklist`\n'
                       f'Sub-commands: `add`, `remove`.\n'
                       f'Usage: `live <command>` for print, or `live <command>_<sub-command>` for edits.')

    @live.command()
    @commands.guild_only()
    async def game(self, ctx):
        await ctx.send(f'Live role games:\n```{self.game_filter}```')

    @live.command()
    @commands.guild_only()
    async def game_add(self, ctx, *, game: str):
        """Add a member to the live role game filter."""
        self.game_filter.append(game)
        await ctx.send(f'Added {game} to game filter. '
                       f'Note: I don\'t check if you spelled it correctly!')

    @live.command()
    @commands.guild_only()
    async def game_remove(self, ctx, *, game: str):
        """Remove a member from the live role game filter."""
        try:
            self.game_filter.remove(game)
        except ValueError:
            return await ctx.send(f'Did not find {game} in the filter!')
        await ctx.send(f'Removed {game} from game filter.')

    @live.command()
    @commands.guild_only()
    async def whitelist(self, ctx):
        await ctx.send(f'Live role member whitelist:\n```{self.member_whitelist}```')

    @commands.guild_only()
    async def whitelist_add(self, ctx, target: discord.User):
        """Add a member to the live role whitelist."""
        self.member_whitelist.append(target)
        await ctx.send(f'{target} added to the live role whitelist.')

    @live.command()
    @commands.guild_only()
    async def whitelist_remove(self, ctx, target: discord.User):
        """Remove a member from the live role whitelist."""
        try:
            self.member_whitelist.remove(target)
        except ValueError:
            return await ctx.send(f'Did not find {target} in the live role whitelist!')
        await ctx.send(f'{target} added to the live role whitelist.')

    @live.command()
    @commands.guild_only()
    async def blacklist(self, ctx):
        await ctx.send(f'Live role member blacklist:\n```{self.member_blacklist}```')

    @live.command()
    @commands.guild_only()
    async def blacklist_add(self, ctx, target: discord.User):
        """Add a member to the live role blacklist."""
        self.member_blacklist.append(target)
        await ctx.send(f'{target} added to the live role blacklist.')

    @live.command()
    @commands.guild_only()
    async def blacklist_remove(self, ctx, target: discord.User):
        """Remove a member from the live role blacklist."""
        try:
            self.member_blacklist.remove(target)
        except ValueError:
            return await ctx.send(f'Did not find {target} in the live role blacklist!')
        await ctx.send(f'{target} added to the live role blacklist.')


def setup(bot):
    bot.add_cog(Live(bot))
