import discord
from discord.ext import commands


class Live(commands.Cog):
    """Gives live roles to eligible members playing eligible games."""
    def __init__(self, bot):
        self.bot = bot

        self.live_role_name = self.get_live_role_name()
        # Game names must exactly match the name as shown on Twitch
        self.game_filter = []
        self.member_blacklist = []
        self.member_whitelist = []

    # TODO: Per-guild role names
    @staticmethod
    def get_live_role_name():
        """Get the live role's name."""
        role = 'Live'
        return role

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """
        Event checking if a member has had a status update
        """
        if before not in self.member_blacklist:
            # Ternaries needed because member.activity = NoneType if it's not an ActivityType
            previous = before.activity.type if before.activity else None
            current = after.activity.type if after.activity else None
            if discord.ActivityType.streaming in (previous, current):
                print(f'Live_update fired by {after.display_name}!')
                return await self.live_update(after)

            print(f'{after.display_name} was {previous.name if previous else None}, '
                  f'now {current.name if current else None}.')

    async def live_update(self, after: discord.Member):
        """
        Updates guild's live role according to members'
        streaming status.
        """
        # Get guild's 'Live' role
        live_role = discord.utils.get(after.guild.roles,
                                      name=self.live_role_name)
        if after.activity:
            live = after.activity.type == discord.ActivityType.streaming
        else:
            live = False

        has_role = live_role in after.roles
        print(f'Live? {live}. Has role? {has_role}.')

        # Remove the role if they are no longer streaming
        if not live:
            if has_role:
                print(f'Role should be removed (no longer live).')
                return await self.live_toggle(after, live_role, remove=True)
            else:
                print(f'Missed them going live, now offline. No action.')
        # Assign the role to a member who starts or updates a stream if appropriate
        eligible = (after.display_name in self.member_whitelist or
                    not self.game_filter or
                    after.activity.details in self.game_filter)
        print(f'Eligible? {eligible}')
        if live and eligible and not has_role:
            print(f'Role should be added.')
            return await self.live_toggle(after, live_role, remove=False)
        print(f'Still live and already have the role.')

    @staticmethod
    async def live_toggle(target: discord.Member, live_role: discord.Role, remove=False):
        try:
            if remove:
                return await target.remove_roles(live_role)
            return await target.add_roles(live_role)
        except discord.Forbidden:
            print(f'Elevation issues in {target.guild}. An admin needs to fix this issue.')

    @commands.group(name='live', invoke_without_command=True)
    async def live(self, ctx):
        await ctx.send('Live role command information'
                       'Commands: `game`, `whitelist`, `blacklist`\n'
                       'Sub-commands: `add`, `remove`.\n'
                       'Usage: `live <command>` for print, or `live <command>_<sub-command>` for edits.')

    @live.command()
    @commands.guild_only()
    async def game(self, ctx):
        await ctx.send(f'Live role games:\n```{self.game_filter}```')

    @live.command()
    @commands.guild_only()
    async def game_add(self, ctx, *, game: str):
        """Add a member to the live role game filter."""
        self.game_filter.append(game)
        await ctx.send(f'Added {game} to game filter.\n'
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
