import nextcord
from nextcord import Interaction

import question


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

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="⬅️", disabled=True, row=0)  #
    async def previous_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        self.page_number -= 1
        await self.update_button(self.page_number)
        await interaction.response.edit_message(view=self, content="",
                                                embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="➡️", disabled=False, row=0)
    async def next_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
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


class FilterPages(nextcord.ui.View):
    def __init__(self, *, timeout: int = 180, pages: list[nextcord.Embed] = None,
                 page_number: int = 0, ctx: nextcord.Interaction = None,
                 choices: list[str] = None):
        super().__init__(timeout=timeout)
        if pages is None:
            pages = []
        self.pages = pages
        self.page_number = page_number
        self.ctx = ctx
        if len(pages) <= 1:
            self.next_button.disabled = True
        if choices is None:
            self.choices = question.create_approve_list()
        else:
            self.choices = choices
        self.select.options = self.create_options()
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
        await interaction.response.edit_message(view=self, content="",
                                                embed=self.pages[self.page_number])

    @nextcord.ui.button(label="", style=nextcord.ButtonStyle.gray, emoji="➡️", disabled=False, row=2)
    async def next_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        self.page_number += 1
        await self.update_choice()
        await self.update_page(self.page_number)
        await interaction.response.edit_message(view=self, content="",
                                                embed=self.pages[self.page_number])

    @nextcord.ui.button(label="Approve", style=nextcord.ButtonStyle.gray, emoji="✅", disabled=True, row=1)
    # <:OutletYes:965914861991235604>
    async def approve_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        await self.disable_button()
        question.filter_question(int(self.val[0]), True)
        await interaction.response.edit_message(view=self, content="", embed=self.pages[self.page_number])

    @nextcord.ui.button(label="Reject", style=nextcord.ButtonStyle.gray, emoji="❌", disabled=True, row=1)
    # <:OutletNo:965913424817176596>
    async def reject_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        await self.disable_button()
        question.filter_question(int(self.val[0]), False)
        await interaction.response.edit_message(view=self, content="", embed=self.pages[self.page_number])

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

    async def on_timeout(self) -> None:
        await self.disable_button()
        og = await self.ctx.original_message()
        await og.edit(view=self, content="", embed=self.pages[self.page_number])

    async def disable_button(self):
        self.previous_button.disabled = True
        self.next_button.disabled = True
        self.approve_button.disabled = True
        self.reject_button.disabled = True
        self.select.disabled = True


class AddQuestion(nextcord.ui.Modal):
    def __init__(self, title: str = "Add a Question"):
        super().__init__(title)
        self.question_box = nextcord.ui.TextInput(label="Question", style=nextcord.TextInputStyle.paragraph,
                                                  min_length=1, max_length=4000,
                                                  required=True, placeholder="Enter the question.")
        self.add_item(self.question_box)

    async def callback(self, interaction: Interaction) -> None:
        question.add_to_filter(self.question_box.value.replace("\n", r"\n"))
        await interaction.send("Question added. It will be passed to approval.")
