import nextcord


class InfoPages(nextcord.ui.View):

    def __init__(self, *, timeout=90, pages=None, page_number=0, ctx=None):
        super().__init__(timeout=timeout)
        if pages is None:
            pages = []
        self.pages = pages
        self.page_number = page_number
        self.ctx = ctx

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="⬅️", disabled=True)
    async def previous_button(self, button: nextcord.ui.button, interaction):
        if self.page_number <= 0:
            await interaction.response.send_message("You are already at the first page! <:EeveeOwO:965977455791857695>",
                                                    ephemeral=True)
        else:
            self.page_number -= 1
            await self.update_button(self.page_number)
            await interaction.response.edit_message(view=self, content="",
                                                    embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="➡️", disabled=False)
    async def next_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if self.page_number >= len(self.pages) - 1:
            await interaction.response.send_message("You are already at the last page! <:EeveeOwO:965977455791857695>",
                                                    ephemeral=True)
        else:
            self.page_number += 1
            await self.update_button(self.page_number)
            await interaction.response.edit_message(view=self, content="",
                                                    embed=self.pages[self.page_number])

    async def update_button(self, page: int):
        self.previous_button.disabled = page == 0
        self.next_button.disabled = page == len(self.pages) - 1

    async def on_timeout(self) -> None:
        await self.disable_button()
        og = await self.ctx.original_message()
        await og.edit(view=self, content="", embed=self.pages[self.page_number])

    async def disable_button(self):
        self.previous_button.disabled = True
        self.next_button.disabled = True
