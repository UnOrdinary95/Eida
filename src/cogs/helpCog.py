import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eida", description="Get a list of commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Eida - Reminder Bot Commands",
            description="Here's a comprehensive guide to all available commands and syntax:",
            color=0x5865F2,
        )

        # Intervals section
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

        # Account management
        embed.add_field(
            name="👤 Account Management",
            value=(
                "`/c` - Create account\n"
                "`/settimezone {TIMEZONE}` - Set your timezone"
            ),
            inline=True,
        )

        # Basic reminder commands
        embed.add_field(
            name="➕ Add Reminders",
            value=(
                "`/remindme {HH:MM} {DD:MM:YYYY} {INTERVALS} {MESSAGE} {NAME}`\n"
                "ℹ️ NOTE : (DATE, INTERVALS and MESSAGE are optional)"
            ),
            inline=True,
        )

        # Modify reminders
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

        # Management commands
        embed.add_field(
            name="🔧 Management",
            value=(
                "`/delrm {NAME}` - Delete reminder\n"
                "`/togglerm {NAME}` - Activate/Deactivate reminder"
            ),
            inline=True,
        )

        # Dashboard commands
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

        # Footer with additional info
        embed.set_footer(
            text="💡 Tip: Use descriptive names for your reminders to easily manage them!",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None,
        )

        embed.set_thumbnail(
            url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
