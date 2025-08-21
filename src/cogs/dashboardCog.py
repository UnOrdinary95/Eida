import discord
from discord import app_commands
from discord.ext import commands
from src.views.dashboardView import DashboardView
from src.database.AccountDAO import AccountDAO
from src.database.ReminderDAO import ReminderDAO


class Dashboard(commands.Cog):
    """
    Dashboard commands for viewing and managing user reminders.
    """

    def __init__(self, bot):
        self.bot = bot
        self.embeds_no_account = discord.Embed(
            title="❌ No Account",
            description="You need to create an account!\nPlease use **/c**.",
        )
        self.embeds_no_reminder = discord.Embed(
            title="❌ No Reminder",
            description="There is no reminder with this name.",
        )

    @app_commands.command(
        name="dashboard", description="Show your dashboard. option: active | inactive"
    )
    async def dashboard(self, interaction: discord.Interaction, option: str = None):
        """
        Display paginated reminder dashboard with optional filtering.
        Three modes: all reminders, active only, or inactive only.
        """
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        # Match statement provides clean filtering logic
        match option:
            case None:
                # Show all reminders regardless of status
                dashboard_view = DashboardView(interaction.user.id)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.name}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )
            case "active":
                # Filter to show only active reminders
                dashboard_view = DashboardView(interaction.user.id, True)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.name}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )
            case "inactive":
                # Filter to show only inactive reminders
                dashboard_view = DashboardView(interaction.user.id, False)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.name}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )

    @app_commands.command(name="showrm", description="Show a specific reminder.")
    async def show_reminder(self, interaction: discord.Interaction, reminder_name: str):
        """
        Display detailed information about a specific reminder.
        Shows all reminder properties in human-readable format.
        """
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        reminder = ReminderDAO.reminder_exists(interaction.user.id, reminder_name)
        if not reminder:
            await interaction.response.send_message(
                embed=self.embeds_no_reminder, ephemeral=True
            )
            return

        # Format reminder details with human-readable interval description
        embed = discord.Embed(
            title=reminder_name,
            description=f"--------------------------------------------------\nDate : {reminder.date}\nTime : {reminder.time}\nInterval : {self.parse_interval_to_human(reminder.intervals)}\nStatus : {'Active' if reminder.status else 'Inactive'}\n--------------------------------------------------\n{reminder.message if reminder.message else 'No description'}",
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

    def parse_interval_to_human(self, interval: str) -> str:
        """
        Convert interval string to human-readable English format.

        Formats supported:
        - {eXm} => every X minutes (min : 10 min)
        - {eXh} => every X hours
        - {eXd} => every X days
        - Combined: e15m2h5d => every 15 minutes / 2 hours / 5 days
        - Weekly: w:mon,tue,wed,thu,fri,sat,sun => Weekly every mon...sun

        Args:
            interval (str): The interval string to parse

        Returns:
            str: Human-readable English description of the interval
        """
        if not interval:
            return "No interval specified"

        # Handle weekly format: w:mon,tue,wed,thu,fri,sat,sun
        if interval.startswith("w:"):
            days_part = interval[2:]  # Remove "w:" prefix
            days = [day.strip() for day in days_part.split(",")]

            # Convert day abbreviations to full names
            day_names = {
                "mon": "Monday",
                "tue": "Tuesday",
                "wed": "Wednesday",
                "thu": "Thursday",
                "fri": "Friday",
                "sat": "Saturday",
                "sun": "Sunday",
            }

            full_day_names = [
                day_names.get(day.lower(), day.capitalize()) for day in days
            ]

            if len(full_day_names) == 1:
                return f"Weekly on {full_day_names[0]}"
            elif len(full_day_names) == 2:
                return f"Weekly on {full_day_names[0]} and {full_day_names[1]}"
            else:
                return f"Weekly on {', '.join(full_day_names[:-1])} and {full_day_names[-1]}"

        # Handle regular intervals: eXm, eXh, eXd or combined like e15m2h5d
        if interval.startswith("e"):
            interval = interval[1:]  # Remove "e" prefix
            parts = []
            current_number = ""

            i = 0
            while i < len(interval):
                char = interval[i]

                if char.isdigit():
                    current_number += char
                elif char in ["m", "h", "d"]:
                    if current_number:
                        number = int(current_number)

                        if char == "m":
                            if number == 1:
                                parts.append("1 minute")
                            else:
                                parts.append(f"{number} minutes")
                        elif char == "h":
                            if number == 1:
                                parts.append("1 hour")
                            else:
                                parts.append(f"{number} hours")
                        elif char == "d":
                            if number == 1:
                                parts.append("1 day")
                            else:
                                parts.append(f"{number} days")

                        current_number = ""
                i += 1

            if parts:
                if len(parts) == 1:
                    return f"Every {parts[0]}"
                elif len(parts) == 2:
                    return f"Every {parts[0]} and {parts[1]}"
                else:
                    return f"Every {', '.join(parts[:-1])} and {parts[-1]}"

        return f"Invalid interval format: {interval}"


async def setup(bot):
    """Setup function for Dashboard cog registration"""
    await bot.add_cog(Dashboard(bot))
    # Register persistent view for bot restart compatibility
    bot.add_view(DashboardView(discord_uid=None))
