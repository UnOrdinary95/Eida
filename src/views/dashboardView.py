import discord
from src.database.ReminderDAO import ReminderDAO
from math import ceil

PAGE_SIZE = 5


class DashboardView(discord.ui.View):
    def __init__(self, discord_uid: int, activity: bool = None):
        super().__init__(timeout=None)
        self.page = 0

        # Get the correct count based on activity filter
        if activity is None:
            reminder_count = ReminderDAO.get_reminder_count(discord_uid=discord_uid)
        else:
            reminder_count = ReminderDAO.get_reminder_count_by_activity(
                discord_uid=discord_uid, activity=activity
            )

        self.total_pages = (
            int(ceil(reminder_count / PAGE_SIZE)) if reminder_count > 0 else 1
        )

        self.discord_uid = discord_uid
        self.activity = activity
        self.update_buttons()

    def update_buttons(self):
        for item in self.children:
            if hasattr(item, "custom_id"):
                if item.custom_id == "prev":
                    item.disabled = self.page == 0
                elif item.custom_id == "next":
                    item.disabled = self.page >= self.total_pages - 1
                elif item.custom_id == "first":
                    item.disabled = self.page == 0
                elif item.custom_id == "last":
                    item.disabled = self.page >= self.total_pages - 1

    def get_current_page_info(self):
        content = self.get_content_from_db(self.page + 1)
        if content == "No content":
            return content, 0, 0
        return content, self.page + 1, self.total_pages

    def get_content_from_db(self, current_page: int):
        if self.activity is None:
            reminders = ReminderDAO.get_reminders_by_offset(
                self.discord_uid, (current_page - 1) * PAGE_SIZE, PAGE_SIZE
            )
        elif self.activity is True:
            reminders = ReminderDAO.get_reminders_by_offset_activity(
                self.discord_uid, (current_page - 1) * PAGE_SIZE, PAGE_SIZE, True
            )
        elif self.activity is False:
            reminders = ReminderDAO.get_reminders_by_offset_activity(
                self.discord_uid, (current_page - 1) * PAGE_SIZE, PAGE_SIZE, False
            )

        content = ""
        for reminder in reminders:
            content += f"{"✅" if reminder[0] else "❌"} - {reminder[1]} | {reminder[2]} | {reminder[3]}\n"

        return content if content else "No content"

    @discord.ui.button(
        label="⏮️", style=discord.ButtonStyle.secondary, custom_id="first"
    )
    async def first_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.page != 0:
            self.page = 0
            self.update_buttons()
            content, current, total = self.get_current_page_info()
            embed = discord.Embed(title=f"{interaction.user.nick}", description=content)
            embed.set_footer(text=f"Page {current}/{total}")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev")
    async def prev_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            content, current, total = self.get_current_page_info()
            embed = discord.Embed(title=f"{interaction.user.nick}", description=content)
            embed.set_footer(text=f"Page {current}/{total}")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next")
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.page < self.total_pages - 1:
            self.page += 1
            self.update_buttons()
            content, current, total = self.get_current_page_info()
            embed = discord.Embed(title=f"{interaction.user.nick}", description=content)
            embed.set_footer(text=f"Page {current}/{total}")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary, custom_id="last")
    async def last_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        last_page = self.total_pages - 1
        if self.page != last_page:
            self.page = last_page
            self.update_buttons()
            content, current, total = self.get_current_page_info()
            embed = discord.Embed(title=f"{interaction.user.nick}", description=content)
            embed.set_footer(text=f"Page {current}/{total}")
            await interaction.response.edit_message(embed=embed, view=self)
