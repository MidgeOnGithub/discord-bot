import discord
from discord.ext import commands

from src.utils import checks, data_io


class Settings(commands.Cog):
    """Provides an interface to check and update bot settings."""
    def __init__(self, bot):
        self.bot = bot
        self.settings_map = {
            'prefixes': self.bot.settings.prefixes,
            'admin_role': self.bot.settings.admin_role,
            'live_role': self.bot.settings.live_role,
            'game_filter': self.bot.settings.game_filter,
            'member_blacklist': self.bot.settings.member_blacklist,
            'member_whitelist': self.bot.settings.member_whitelist,
        }

    async def cog_check(self, ctx):
        return checks.is_admin()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def settings(self, ctx):
        """
        Command to pretty-print the bot's settings.

        Command Usage:
        `settings`
        """
        await ctx.send(f'Current settings:\n```'
                       f'Prefixes: {", ".join(self.bot.settings.prefixes)}\n'
                       f'Admin role: {self.bot.settings.admin_role}\n'
                       f'Live role: {self.bot.settings.live_role}\n'
                       f'Game filter: {", ".join(self.bot.settings.game_filter)}\n'
                       f'Member blacklist: {", ".join(self.bot.settings.member_blacklist)}\n'
                       f'Member whitelist: {", ".join(self.bot.settings.member_whitelist)}'
                       f'```For command help: `settings help`.')

    @settings.command()
    @commands.guild_only()
    async def help(self, ctx):
        """
        Command to display other settings cog commands

        Command Usage:
        `settings help`
        """
        await ctx.send(f'Settings commands:\n'
                       f'`clear <setting>` -- only works for settings which can be lists.\n'
                       f'`prefixes <prefix>` -- add/remove <prefix> from the bot command prefixes.\n'
                       f'`admin_role <new_role>` -- change admin role to <new_role>.\n'
                       f'`live_role <new_role>` -- change live role to <new_role>.\n'
                       f'`game_filter <game>` -- add/remove <game> from the live_role game filter.\n'
                       f'`member_blacklist <member>` -- add/remove <member> from the live role blacklist.\n'
                       f'`member_whitelist <member>` -- add/remove <member> from the live role whitelist.\n')

    @settings.command()
    @commands.guild_only()
    async def clear(self, ctx, setting_to_clear: str):
        """
        Command to clear a setting of potentially multiple items.

        Command Usage:
        `settings clear <setting_to_clear>`
        """
        setting = self.settings_map[setting_to_clear]
        if isinstance(setting, list):
            setting.clear()
            if setting_to_clear == 'prefixes':
                setting.append('!')
        else:
            return await ctx.send(f'No change. {setting_to_clear} is a single-item setting.')
        await ctx.send(f'Changes saved. `{setting_to_clear}` cleared/reset.')

    @settings.command()
    @commands.guild_only()
    async def admin_role(self, ctx, new_role_name: str):
        """
        Command to change the admin role.

        Command Usage:
        `settings admin_role <new_role_name>`
        """
        if await self._change_single_item_setting(ctx, 'admin_role', new_role_name):
            await ctx.send(f'Changes saved. Admin role: `{self.bot.settings.admin_role}`')

    @settings.command()
    @commands.guild_only()
    async def live_role(self, ctx, new_role_name: str):
        """
        Command to change the live role.

        Command Usage:
        `settings live_role <new_role_name>`
        """
        if await self._change_single_item_setting(ctx, 'live_role', new_role_name):
            await ctx.send(f'Changes saved. Live role: `{self.bot.settings.live_role}`')

    async def _change_single_item_setting(self, ctx, setting_to_change: str, new_value: str):
        """
        Changes a single-item setting's value, unless the same value is given.
        Returns true if the value was new.
        """
        setting = self.settings_map[setting_to_change]
        if isinstance(setting, list):
            return await ctx.send('Bad argument passed to _change_single_item_setting.')
        if setting == new_value:
            return await ctx.send('No change.')
        else:
            self.settings_map[setting] = new_value
        await self.update_settings_file()
        return True

    # TODO: DRY: prefixes, game_filter, member_*list commands
    @settings.command()
    @commands.guild_only()
    async def prefixes(self, ctx, prefix: str):
        """
        Command to add/remove a command prefix.

        Command Usage:
        `settings prefixes <prefix>`
        """
        await self._setting_list_item_toggle(prefix, self.bot.settings.prefix)
        if self.bot.settings.prefixes:
            msg = ', '.join([g for g in self.bot.settings.prefixes])
        else:
            msg = 'No prefixes (mentions only).'
        await ctx.send('Changes saved. Available prefixes:\n'
                       f'```{msg}```')

    @settings.command()
    @commands.guild_only()
    async def game_filter(self, ctx, *, game: str):
        """
        Command to add/remove a game from the live role game filter.

        Command Usage:
        `settings game_filter <game>`
        """
        await self._setting_list_item_toggle(game, self.bot.settings.game_filter)
        if self.bot.settings.game_filter:
            msg = ', '.join([g for g in self.bot.settings.game_filter])
        else:
            msg = 'No games listed.'
        await ctx.send(f'Changes saved. (Note: I don\'t check if you spelled it correctly!) Live role game filter:\n'
                       f'```{msg}```')

    # TODO: Consider: take a str instead; check for a member, then add
    #  But if it can't find the member, it tries to remove the name
    #  This could prevent names being "grandfathered" into the list and never being able
    #  to be removed because they changed their Discord name
    @settings.command()
    @commands.guild_only()
    async def member_blacklist(self, ctx, member: discord.User):
        """
        Command to add/remove a member from the live role whitelist.

        Command Usage:
        `settings member_blacklist <member>`
        """
        await self._setting_list_item_toggle(member.id, self.bot.settings.member_blacklist)
        member_list = [await commands.UserConverter().convert(ctx, str(num))
                       for num in self.bot.settings.member_blacklist]
        if member_list:
            msg = ', '.join([mem.display_name for mem in member_list])
        else:
            msg = 'No members listed.'
        await ctx.send(f'Changes saved. Live role guild blacklist:\n'
                       f'```{msg}```')

    @settings.command()
    @commands.guild_only()
    async def member_whitelist(self, ctx, member: discord.User):
        """
        Command to add/remove a member from the live role whitelist.

        Command Usage:
        `settings member_whitelist <member>`
        """
        await self._setting_list_item_toggle(member.id, self.bot.settings.member_whitelist)
        member_list = [await commands.UserConverter().convert(ctx, str(num))
                       for num in self.bot.settings.member_whitelist]
        if member_list:
            msg = ', '.join([mem.display_name for mem in member_list])
        else:
            msg = 'No members listed.'
        await ctx.send(f'Changes saved. Live role guild whitelist:\n'
                       f'```{msg}```')

    async def _setting_list_item_toggle(self, item, setting_list: list):
        """
        Toggles an item from a settings list of items.
        """
        if item not in setting_list:
            setting_list.append(item)
        else:
            setting_list.remove(item)
        await self.update_settings_file()

    async def update_settings_file(self):
        """
        Saves any changes into the settings file
        """
        self.bot.loop.run_in_executor(None, data_io.save_settings,
                                      self.bot.settings, self.bot.settings_file)


def setup(bot):
    bot.add_cog(Settings(bot))
