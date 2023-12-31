import nextcord


class InfoPages(nextcord.ui.View):

    def __init__(self, *, timeout: int = 90, pages: list[nextcord.Embed] = None,
                 page_number: int = 0, ctx: nextcord.Interaction = None):
        super().__init__(timeout=timeout)
        if pages is None:
            pages = []
        self.pages = pages
        self.page_number = page_number
        self.ctx = ctx
        if len(pages) <= 1:
            self.next_button.disabled = True

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="⬅️", disabled=True, row=4)
    async def previous_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        self.page_number -= 1
        await self.update_button(self.page_number)
        await interaction.response.edit_message(view=self, embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="➡️", disabled=False, row=4)
    async def next_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        self.page_number += 1
        await self.update_button(self.page_number)
        await interaction.response.edit_message(view=self, embed=self.pages[self.page_number])

    async def update_button(self, page: int):
        self.previous_button.disabled = page == 0
        self.next_button.disabled = page == len(self.pages) - 1

    async def on_timeout(self) -> None:
        self.disable_button()
        og = await self.ctx.original_message()
        await og.edit(view=self, content="", embed=self.pages[self.page_number])

    def disable_button(self):
        self.previous_button.disabled = True
        self.next_button.disabled = True
