import discord
from discord import app_commands
from discord.ext import commands
from src.views.dashboardView import DashboardView
from src.database.AccountDAO import AccountDAO


class Dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds_no_account = discord.Embed(
            title="❌ No Account",
            description="You need to create an account!\nPlease use **/c**.",
        )

    @app_commands.command(name="dashboard", description="Show your dashboard. option: active | inactive")
    async def dashboard(self, interaction: discord.Interaction, option: str = None):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        match option:
            case None:
                dashboard_view = DashboardView(interaction.user.id)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.nick}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )
            case "active":
                dashboard_view = DashboardView(interaction.user.id, True)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.nick}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )
            case "inactive":
                dashboard_view = DashboardView(interaction.user.id, False)
                content, current, total = dashboard_view.get_current_page_info()

                embed = discord.Embed(
                    title=f"{interaction.user.nick}", description=content
                )
                embed.set_footer(text=f"Page {current}/{total}")

                await interaction.response.send_message(
                    embed=embed, view=dashboard_view, ephemeral=True
                )


async def setup(bot):
    await bot.add_cog(Dashboard(bot))
    bot.add_view(DashboardView(discord_uid=None))
