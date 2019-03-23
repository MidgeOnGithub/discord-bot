import asyncio

import discord
from discord.ext import commands

import utils.data_io


class Settings(commands.Cog):
    """Provides an interface to check and update bot settings."""
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """
        A check that allows only bot owner or guild admin to invoke commands.
        """
        author = ctx.message.author
        # Do the easy check first
        if await self.bot.is_owner(ctx.message.author):
            return True
        # Then the slower check
        admin_role = self.bot.settings['admin_role']
        is_admin = discord.utils.get(author.roles, name=admin_role)
        if is_admin:
            return True
        else:
            return False

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
        `settings clear`
        """
        try:
            setting = self.bot.settings[setting_to_clear]
            if isinstance(setting, list):
                setting.clear()
                if setting == 'prefixes':
                    setting.append('!')
            else:
                return await ctx.send(f'No change since {setting_to_clear}'
                                      f'is a single-item setting.')
        except KeyError:
            return await ctx.send('Bad setting name')
        await ctx.send(f'Changes saved. `{setting_to_clear}` cleared/reset.')

    @settings.command()
    @commands.guild_only()
    async def prefixes(self, ctx, prefix: str):
        """
        Command to add -- or if already present, remove -- a command prefix.

        Command Usage:
        `settings prefix`
        """
        active_prefixes = self.bot.settings.prefixes
        if prefix in active_prefixes:
            active_prefixes.remove(prefix)
        else:
            active_prefixes.append(prefix)
        await self.update_settings_file()
        await ctx.send('Changes saved. Available prefixes:\n'
                       f'```{", ".join(active_prefixes)}```')

    @settings.command()
    @commands.guild_only()
    async def admin_role(self, ctx, *, new_role_name: str):
        """
        Command to change the admin role.

        Command Usage:
        `settings admin_role`
        """
        current_role_name = self.bot.settings.admin_role
        if new_role_name == current_role_name:
            return await ctx.send(f'No change.')
        else:
            current_role_name = new_role_name
        await self.update_settings_file()
        await ctx.send(f'Changes saved. Admin role: `{current_role_name}`')

    # TODO: Fix the WET: game_filter, member_*list commands
    @settings.command()
    @commands.guild_only()
    async def game_filter(self, ctx, *, game: str):
        """
        Command to add -- or if already present, remove -- a game from the live role game filter.

        Command Usage:
        `settings game_filter`
        """
        current_filter = self.bot.settings.game_filter
        if game not in current_filter:
            current_filter.append(game)
        else:
            current_filter.remove(game)
        await self.update_settings_file()
        await ctx.send('Changes saved. Note that I don\'t check if you spelled it correctly!\n'
                       'Live role game filter:\n'
                       f'```{", ".join(current_filter)}```')

    # TODO: Consider: take a str instead; check it's a member, then add
    #  But if it can't find the member, it tries to remove the name
    #  This could prevent names being "grandfathered" into the list and never being able
    #  to be removed because they changed their Discord name
    @settings.command()
    @commands.guild_only()
    async def member_blacklist(self, ctx, member: discord.Member):
        """
        Command to add -- or if already present, remove -- a member from the live role whitelist.

        Command Usage:
        `settings member_blacklist`
        """
        current_filter = self.bot.settings.member_blacklist
        if member not in current_filter:
            current_filter.append(member.name)
        else:
            current_filter.remove(member.name)
        await self.update_settings_file()
        await ctx.send(f'Changes saved. Live role blacklist:\n'
                       f'```{", ".join(current_filter)}```')

    @settings.command()
    @commands.guild_only()
    async def member_whitelist(self, ctx, member: discord.Member):
        """
        Command to add -- or if already present, remove -- a member from the live role whitelist.

        Command Usage:
        `settings member_whitelist`
        """
        current_filter = self.bot.settings.member_whitelist
        name = member.name
        if name not in current_filter:
            current_filter.append(name)
        else:
            current_filter.remove(name)
        await self.update_settings_file()
        await ctx.send(f'Changes saved. Member whitelist:\n'
                       f'```{", ".join(current_filter)}```')

    async def update_settings_file(self):
        """
        Saves any changes into the settings file
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, utils.data_io.save_settings,
                                   self.bot.settings, self.bot.settings_file)


def setup(bot):
    bot.add_cog(Settings(bot))
