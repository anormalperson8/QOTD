import nextcord

import question


class FilterPages(nextcord.ui.View):
    def __init__(self, *, timeout: int = 180, title: str = "", url: str = None,
                 image: str = None, ctx: nextcord.Interaction = None):
        super().__init__(timeout=timeout)
        self.title = title
        self.url = url
        self.image = image
        self.ctx = ctx

        self.pages = []
        self.page_number = 0
        self.choices = None
        self.select.options = []

        self.reset()
        if len(self.pages) <= 1:
            self.next_button.disabled = True

        self.val = None

    @nextcord.ui.select(placeholder="Select an option", row=0)
    async def select(self, menu: nextcord.ui.Select, interaction: nextcord.Interaction):
        self.val = menu.values
        self.select.placeholder = f"Question {int(self.val[0]) + 1}"
        self.approve_button.disabled = False
        self.reject_button.disabled = False
        await interaction.response.edit_message(view=self, content="", embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="⬅️", disabled=True, row=2)
    async def previous_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        self.page_number -= 1
        await self.update_choice()
        await self.update_page(self.page_number)
        await interaction.response.edit_message(view=self, embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="➡️", disabled=False, row=2)
    async def next_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        self.page_number += 1
        await self.update_choice()
        await self.update_page(self.page_number)
        await interaction.response.edit_message(view=self, embed=self.pages[self.page_number])

    @nextcord.ui.button(label="Approve", style=nextcord.ButtonStyle.gray, emoji="✅", disabled=True, row=1)
    # <:OutletYes:965914861991235604>
    async def approve_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        t = self.result_string(True)
        question.filter_question(int(self.val[0]), True)
        self.reset()
        await interaction.response.edit_message(view=self, content=t, embed=self.pages[self.page_number])

    @nextcord.ui.button(label="Reject", style=nextcord.ButtonStyle.gray, emoji="❌", disabled=True, row=1)
    # <:OutletNo:965913424817176596>
    async def reject_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        t = self.result_string(False)
        question.filter_question(int(self.val[0]), False)
        self.reset()
        await interaction.response.edit_message(view=self, content=t, embed=self.pages[self.page_number])

    def result_string(self, status: bool):
        q = question.get_filter_question(int(self.val[0])).replace("\n", r"\n")
        t = f"**Question {int(self.val[0]) + 1}:\n`{q}`\nhas been"
        if status:
            t += " approved.**"
        else:
            t += " rejected.**"
        return t

    async def update_page(self, page: int):
        self.previous_button.disabled = page == 0
        self.next_button.disabled = page == len(self.pages) - 1

    async def update_choice(self):
        self.select.placeholder = "Select an option"
        self.val = None
        self.approve_button.disabled = True
        self.reject_button.disabled = True
        self.select.options = self.create_options()

    def create_options(self):
        return [nextcord.SelectOption(label=f"Question {i + self.page_number * 10 + 1}",
                                      value=str(i + self.page_number * 10))
                for i in range(len(self.choices[self.page_number]))]

    def reset(self):
        self.select.placeholder = "Select an option"
        self.choices = question.create_approve_list()
        self.select.options = self.create_options()
        self.pages = question.create_approve_pages(self.title, self.url)
        for i in range(len(self.pages)):
            self.pages[i].set_thumbnail(self.image)
            self.pages[i].set_footer(text=f"Page {i + 1}/{len(self.pages)}")
        self.page_number = 0
        if not question.filter_empty():
            self.disable_page_turning()
            self.disable_approval_button()
        else:
            self.disable_button()
        if len(self.pages) > 1:
            self.next_button.disabled = False

    async def on_timeout(self) -> None:
        self.disable_button()
        og = await self.ctx.original_message()
        await og.edit(view=self, embed=self.pages[self.page_number])

    def disable_page_turning(self):
        self.previous_button.disabled = True
        self.next_button.disabled = True

    def disable_approval_button(self):
        self.approve_button.disabled = True
        self.reject_button.disabled = True

    def disable_button(self):
        self.disable_page_turning()
        self.disable_approval_button()
        self.select.disabled = True
