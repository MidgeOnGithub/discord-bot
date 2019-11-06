from discord.ext import commands

from src.utils import checks, data_io


TR_GUILD_ID = 183942718630658048
CHAN_TOMP1_ID = 221977162142580736
CHAN_TOMP2_ID = 221977184997343234
CHAN_TOMP3_ID = 221977215779340288
CHAN_TOMP4_ID = 184212236821069824
CHAN_TOMP5_ID = 221977251598565386
CHAN_AOD_ID = 184212318593220608
CHAN_LEGEND_ID = 360838603078762497
CHAN_ANNIVERSARY_ID = 184212333424279554
CHAN_UNDERWORLD_ID = 184212580678500352
CHAN_TR2013_ID = 360838349751058453
CHAN_ROTTR_ID = 184212611687120896
CHAN_SHADOW_ID = 441308548077715460
CHAN_LCGOL_ID = 184212746118627328
CHAN_LCTOO_ID = 184212872405057536
CHAN_MOBILE_ID = 184212986402045953
CHAN_ROLE_REQUEST_ID = 409098961383718912

# Chronological list of TR games as seen in Twitch's directory
tr_games = [
    'Tomb Raider (1996)',
    'Tomb Raider: Unfinished Business',
    'Tomb Raider II',
    'Tomb Raider: The Golden Mask',
    'Tomb Raider III: Adventures of Lara Croft',
    'Tomb Raider: The Lost Artifact',
    'Tomb Raider: The Last Revelation',
    'Tomb Raider: Chronicles',
    'Lara Croft Tomb Raider: The Angel of Darkness',
    'Lara Croft Tomb Raider: Legend',
    'Lara Croft Tomb Raider: Anniversary',
    'Tomb Raider: Underworld',
    'Lara Croft and the Guardian of Light',
    'Tomb Raider',
    'Lara Croft and the Temple of Osiris',
    'Lara Croft: Go',
    'Rise of the Tomb Raider',
    'Shadow of the Tomb Raider'
]

# Map of channel IDs in the TR speedrunning Discord guild
tr_chan_id_map = {
    'tomp1':        CHAN_TOMP1_ID,
    'tomp2':        CHAN_TOMP2_ID,
    'tomp3':        CHAN_TOMP3_ID,
    'tomp4':        CHAN_TOMP4_ID,
    'tomp5':        CHAN_TOMP5_ID,
    'aod':          CHAN_AOD_ID,
    'legend':       CHAN_LEGEND_ID,
    'anniversary':  CHAN_ANNIVERSARY_ID,
    'underworld':   CHAN_UNDERWORLD_ID,
    'tr2013':       CHAN_TR2013_ID,
    'rottr':        CHAN_ROTTR_ID,
    'shadow':       CHAN_SHADOW_ID,
    'lcgol':        CHAN_LCGOL_ID,
    'lctoo':        CHAN_LCTOO_ID,
    'mobile_games': CHAN_MOBILE_ID,
    'role_request': CHAN_ROLE_REQUEST_ID
}

# A map to help with _get_message()
tr_chan_abbreviation_map = {
    'Role': 'role_request',
    'TR1': 'tomp1',
    'TR2': 'tomp2',
    'TR3': 'tomp3',
    'TR4': 'tomp4',
    'TR5': 'tomp5',
    'AoD': 'aod',
    'TRL': 'legend',
    'TRA': 'anniversary',
    'TRU': 'underworld',
    'TR2013': 'tr2013',
    'RotTR': 'rottr',
    'SotTR': 'shadow',
    'LCGoL': 'lcgol',
    'LCToO': 'lctoo'
}

# Mapping of role request commands to actual role names
tr_roles_dict = {
    # Channels
    'tr1': 'TR1 Runners',
    'tr2': 'TR2 Runners',
    'tr3': 'TR3 Runners',
    'tr4': 'TR4 Runners',
    'tr5': 'TR5 Runners',
    'aod': 'AoD Runners',
    'trl': 'TRL Runners',
    'tra': 'TRA Runners',
    'tru': 'TRU Runners',
    'tr2013': 'TR2013 Runners',
    'rottr': 'RotTR Runners',
    'shadow': 'Shadow Runners',
    'gol': 'GoL Runners',
    'too': 'ToO Runners',
    # Colors
    'blue': 'Blue',
    'gray': 'Gray',
    'green': 'Green',
    'orange': 'Orange',
    'pink': 'Pink',
    'purple': 'Purple',
    'red': 'Red',
    'teal': 'Teal'
}


class TombRunner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Tomp1(bot))
        self.bot.add_cog(Tomp2(bot))
        self.bot.add_cog(Tomp3(bot))
        self.bot.add_cog(Tomp4(bot))
        self.bot.add_cog(Tomp5(bot))
        self.bot.add_cog(Aod(bot))
        self.bot.add_cog(Legend(bot))
        self.bot.add_cog(Anniversary(bot))
        self.bot.add_cog(Underworld(bot))
        self.bot.add_cog(TR2013(bot))
        self.bot.add_cog(Rottr(bot))
        self.bot.add_cog(Shadow(bot))
        self.bot.add_cog(Lcgol(bot))
        self.bot.add_cog(Lctoo(bot))

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_ROLE_REQUEST_ID):
            await ctx.send(f'{_get_message("Role")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        await ctx.message.delete()

    @commands.group(invoke_without_command=True)
    async def role(self, ctx):
        pass

    @role.command()
    async def tr1(self, ctx):
        """Self-assign the role for TR1."""
        await self.__tr_role_toggle(ctx, 'tr1')

    @role.command()
    async def tr2(self, ctx):
        """Self-assign the role for TR2."""
        await self.__tr_role_toggle(ctx, 'tr2')

    @role.command()
    async def tr3(self, ctx):
        """Self-assign the role for TR3."""
        await self.__tr_role_toggle(ctx, 'tr3')

    @role.command()
    async def tr4(self, ctx):
        """Self-assign the role for TR4."""
        await self.__tr_role_toggle(ctx, 'tr4')

    @role.command()
    async def tr5(self, ctx):
        """Self-assign the role for TR5."""
        await self.__tr_role_toggle(ctx, 'tr5')

    @role.command()
    async def aod(self, ctx):
        """Self-assign the role for AOD."""
        await self.__tr_role_toggle(ctx, 'aod')

    @role.command()
    async def trl(self, ctx):
        """Self-assign the role for TRL."""
        await self.__tr_role_toggle(ctx, 'trl')

    @role.command()
    async def tra(self, ctx):
        """Self-assign the role for TRA."""
        await self.__tr_role_toggle(ctx, 'tra')

    @role.command()
    async def tru(self, ctx):
        """Self-assign the role for TRU."""
        await self.__tr_role_toggle(ctx, 'tru')

    @role.command()
    async def tr2013(self, ctx):
        """Self-assign the role for TR (2013)."""
        await self.__tr_role_toggle(ctx, 'tr2013')

    @role.command()
    async def rottr(self, ctx):
        """Self-assign the role for RotTR."""
        await self.__tr_role_toggle(ctx, 'rottr')

    @role.command()
    async def shadow(self, ctx):
        """Self-assign the role for SotTR."""
        await self.__tr_role_toggle(ctx, 'shadow')

    @role.command()
    async def gol(self, ctx):
        """Self-assign the role for GoL."""
        await self.__tr_role_toggle(ctx, 'gol')

    @role.command()
    async def too(self, ctx):
        """Self-assign the role for ToO."""
        await self.__tr_role_toggle(ctx, 'too')

    @role.command()
    async def blue(self, ctx):
        """Self-assign the blue color."""
        await self.__tr_role_toggle(ctx, 'blue')

    @role.command(alias="grey")
    async def gray(self, ctx):
        """Self-assign the gray color."""
        await self.__tr_role_toggle(ctx, 'gray')

    @role.command()
    async def green(self, ctx):
        """Self-assign the green color."""
        await self.__tr_role_toggle(ctx, 'green')

    @role.command()
    async def orange(self, ctx):
        """Self-assign the orange color."""
        await self.__tr_role_toggle(ctx, 'orange')

    @role.command()
    async def pink(self, ctx):
        """Self-assign the pink color."""
        await self.__tr_role_toggle(ctx, 'pink')

    @role.command()
    async def purple(self, ctx):
        """Self-assign the purple color."""
        await self.__tr_role_toggle(ctx, 'purple')

    @role.command()
    async def red(self, ctx):
        """Self-assign the red color."""
        await self.__tr_role_toggle(ctx, 'red')

    @role.command()
    async def teal(self, ctx):
        """Self-assign the teal color."""
        await self.__tr_role_toggle(ctx, 'teal')

    @commands.bot_has_permissions(manage_roles=True)
    async def __tr_role_toggle(self, ctx, desired_role: str):
        """
        Allows user to self-assign desired roles.

        Command Usage:
        `role <desired role>`
        """
        if desired_role not in tr_roles_dict.keys():
            return await ctx.send(f'Role **{desired_role}** not in my keys... @Midge#3751 fix your mistake, dummy.')

        role = await commands.RoleConverter().convert(ctx, tr_roles_dict[desired_role])
        if role is None:
            return await ctx.send(f'Error retrieving **{desired_role}** despite understanding it as a valid role...')

        reason = f'Requested by {ctx.author.id}.'
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role, reason=reason)
        else:
            await ctx.author.add_roles(role, reason=reason)


class Tomp1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TOMP1_ID):
            await ctx.send(f'{_get_message("TR1")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Tomp2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TOMP2_ID):
            await ctx.send(f'{_get_message("TR2")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Tomp3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TOMP3_ID):
            await ctx.send(f'{_get_message("TR3")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Tomp4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TOMP4_ID):
            await ctx.send(f'{_get_message("TR4")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Tomp5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TOMP5_ID):
            await ctx.send(f'{_get_message("TR5")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Aod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_AOD_ID):
            await ctx.send(f'{_get_message("AoD")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Legend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_LEGEND_ID):
            await ctx.send(f'{_get_message("TRL")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Anniversary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_ANNIVERSARY_ID):
            await ctx.send(f'{_get_message("TRA")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Underworld(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_UNDERWORLD_ID):
            await ctx.send(f'{_get_message("TRU")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class TR2013(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_TR2013_ID):
            await ctx.send(f'{_get_message("TR2013")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Rottr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_ROTTR_ID):
            await ctx.send(f'{_get_message("RotTR")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Shadow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_SHADOW_ID):
            await ctx.send(f'{_get_message("SotTR")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Lcgol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_LCGOL_ID):
            await ctx.send(f'{_get_message("LCGoL")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


class Lctoo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not checks.invoked_in_channels(CHAN_LCTOO_ID):
            await ctx.send(f'{_get_message("LCToO")}')
            return False
        return True

    async def cog_after_invoke(self, ctx):
        ctx.message.delete()


def _get_message(game: str):
    return f'{game}-specific commands must be invoked in <#{tr_chan_id_map[tr_chan_abbreviation_map[game]]}>.'


def setup(bot):
    # Ensure all TR games are in the live role game filter
    games_filter = bot.settings.game_filter
    if not all(game in set(games_filter) for game in tr_games):
        for game in tr_games:
            games_filter.append(game)
        # Preserve order but remove duplicates
        bot.settings.game_filter = list(dict.fromkeys(games_filter))
        # TODO: use command from Settings cog, remove imports
        data_io.save_settings(bot.settings, bot.settings_file)

    bot.add_cog(TombRunner(bot))
