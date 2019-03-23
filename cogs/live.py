import discord
from discord.ext import commands


# TODO: Persistence of per-guild settings?
class Live(commands.Cog):
    """Gives live roles to eligible members playing eligible games."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """
        Event checking if a member has had a Streaming status update
        """
        if before.name not in self.bot.settings.member_blacklist:
            # Ternaries because member.activity is either NoneType or ActivityType
            previous = before.activity.type if before.activity else None
            current = after.activity.type if after.activity else None
            if discord.ActivityType.streaming in (previous, current):
                return await self._live_update(after)

    async def _live_update(self, after: discord.Member):
        """
        Updates a guild member's live role status.
        """
        # Get guild's 'Live' role
        live_role = discord.utils.get(after.guild.roles,
                                      name=self.bot.settings.live_role)
        # Using this if in case `after` now has NoneType activity
        if after.activity:
            live = after.activity.type == discord.ActivityType.streaming
        else:
            live = False

        has_role = live_role in after.roles
        # Remove the role if they are no longer streaming
        if not live:
            if has_role:
                print(f'Role should be removed ({after.name} no longer live).')
                return await self._live_toggle(after, live_role, remove=True)
            else:
                print(f'{after.name} didn\'t have role and is offline. No action.')

        # From here, member is definitely live, so just
        # assign the role if they are eligible and don't have it,
        # remove the role if they are no longer eligible
        eligible = (after.name in self.bot.settings.member_whitelist or  # Whitelisted members always get the role
                    not self.bot.settings.game_filter or                 # If filter is empty, all games are valid
                    after.activity.details in self.bot.settings.game_filter)

        if eligible and not has_role:
            print(f'Role should be added to {after.name}.')
            return await self._live_toggle(after, live_role, remove=False)
        if not eligible and has_role:
            print(f'{after.name} is still live, but no longer eligible (game or blacklist).')
            return await self._live_toggle(after, live_role, remove=True)

        print(f'{after.name} is live, eligible, but already has the role.')

    @staticmethod
    async def _live_toggle(target: discord.Member,
                           live_role: discord.Role, remove=False):
        """
        Toggles the live_role on or off, with respect to `remove`.
        """
        try:
            if remove:
                return await target.remove_roles(live_role)
            return await target.add_roles(live_role)
        except discord.Forbidden:
            print(f'Elevation issues in {target.guild}. An admin needs to fix this issue.')

    @commands.group(name='live', invoke_without_command=True)
    async def live(self, ctx):
        """
        Displays help information for `live` group commands.

        Command Usage:
        `live`
        """
        await ctx.send(f'Live role: {self.bot.settings.live_role}\n'
                       f'Commands: `games`, `whitelist`, `blacklist`\n'
                       f'Note: use `settings` commands to make edits.')

    @live.command()
    @commands.guild_only()
    async def games(self, ctx):
        """
        Display the games in the game filtering list.

        Command Usage:
        `live game`
        """
        await ctx.send(f'Live role games:\n```{self.bot.settings.game_filter}```')

    @live.command()
    @commands.guild_only()
    async def blacklist(self, ctx):
        """
        Display the list of guild-wide blacklisted members.

        Command Usage:
        `live blacklist`
        """
        await ctx.send(f'Live role member blacklist:\n'
                       f'```{", ".join(self.bot.settings.member_blacklist)}```')

    @live.command()
    @commands.guild_only()
    async def whitelist(self, ctx):
        """
        Display the list of guild-wide whitelisted members.

        Command Usage:
        `live whitelist`
        """
        await ctx.send(f'Live role member whitelist:\n'
                       f'```{", ".join(self.bot.settings.member_whitelist)}```')

def setup(bot):
    bot.add_cog(Live(bot))
