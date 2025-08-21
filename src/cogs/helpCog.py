import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):
    """
    Help system providing comprehensive command documentation.
    Single command that displays all bot functionality with examples.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eida", description="Get a list of commands")
    async def help(self, interaction: discord.Interaction):
        """
        Display comprehensive help documentation with structured sections.
        Named 'eida' instead of 'help' to avoid conflicts with other's bot built-in help.
        """
        embed = discord.Embed(
            title="Eida - Reminder Bot Commands",
            description="Here's a comprehensive guide to all available commands and syntax:",
            color=0x5865F2,
        )

        # Intervals section - most complex feature, shown first for reference
        embed.add_field(
            name="⏰ Intervals Syntax",
            value=(
                "**Minutes:** `{e15m}` - every 15 minutes (min: 10 min)\n"
                "**Hours:** `{e2h}` - every 2 hours\n"
                "**Days:** `{e5d}` - every 5 days\n"
                "**Weekly:** `{w:mon,tue,wed,thu,fri,sat,sun} | {w:*}` - specific days | everydays\n\n"
                "**Examples:**\n"
                "`e15m2h5d` - every 15 min / 2 hours / 5 days\n"
                "`w:mon,tue,sat,fri` - weekly on specific days\n"
            ),
            inline=False,
        )

        # Account management - prerequisite commands shown early
        embed.add_field(
            name="👤 Account Management",
            value=(
                "`/c` - Create account\n"
                "`/settimezone {TIMEZONE}` - Set your timezone"
            ),
            inline=True, 
        )

        # Basic reminder commands - core functionality
        embed.add_field(
            name="➕ Add Reminders",
            value=(
                "`/remindme {HH:MM} {DD:MM:YYYY} {INTERVALS} {MESSAGE} {NAME}`\n"
                "ℹ️ NOTE : (DATE and INTERVALS are optional)"
            ),
            inline=True,
        )

        # Modify reminders - grouped editing commands
        embed.add_field(
            name="✏️ Modify Reminders",
            value=(
                "`/setname {NAME} {NEW_NAME}` - Change name\n"
                "`/setmsg {NAME} {MESSAGE}` - Change message\n"
                "`/settime {NAME} {HH:MM}` - Change time\n"
                "`/setdate {NAME} {DD:MM:YYYY}` - Change date\n"
                "`/setintervals {NAME} {INTERVALS}` - Change intervals"
            ),
            inline=False,
        )

        # Management commands - control operations
        embed.add_field(
            name="🔧 Management",
            value=(
                "`/delrm {NAME}` - Delete reminder\n"
                "`/togglerm {NAME}` - Activate/Deactivate reminder"
            ),
            inline=True,
        )

        # Dashboard commands - viewing and inspection
        embed.add_field(
            name="📊 Dashboard",
            value=(
                "`/dashboard` - Show all reminders\n"
                "`/dashboard active` - Show active reminders\n"
                "`/dashboard inactive` - Show inactive reminders\n"
                "`/showrm {NAME}` - Show reminder details"
            ),
            inline=True,
        )

        # Footer with user guidance and bot branding
        embed.set_footer(
            text="💡 Tip: Use descriptive names for your reminders to easily manage them!",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None,
        )

        # Thumbnail for visual appeal and bot recognition
        embed.set_thumbnail(
            url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    """Standard Discord.py cog setup function"""
    await bot.add_cog(Help(bot))
