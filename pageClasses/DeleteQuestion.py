import nextcord

import question
from pageClasses.QuestionPages import QuestionPages


class DeleteQuestion(QuestionPages):
    def __init__(self, *, timeout: int = 90, page_number: int = 0,
                 title: str = "", url: str = None, image=None,
                 ctx: nextcord.Interaction = None):
        super().__init__(timeout=timeout, page_number=page_number, title=title, url=url, image=image, ctx=ctx)
        self.choices = None
        self.val = None
        self.reset()

    @nextcord.ui.select(placeholder="Select an option", row=0)
    async def select(self, menu: nextcord.ui.Select, interaction: nextcord.Interaction):
        self.val = menu.values
        self.select.placeholder = f"Question {int(self.val[0]) + 1}"
        self.delete_button.disabled = False
        await interaction.response.edit_message(view=self, embed=self.pages[self.page_number])

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.gray, emoji="❌", disabled=True, row=1)
    async def delete_button(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("This is not yours <:EeveeOwO:965977455791857695>", ephemeral=True)
            return
        t = self.result_string()
        question.remove_question(int(self.val[0]))
        self.reset()
        await interaction.response.edit_message(view=self, content=t, embed=self.pages[self.page_number])

    def result_string(self):
        q = question.get_question(int(self.val[0])).replace("\n", r"\n")
        t = f"**Question {int(self.val[0]) + 1}:\n`{q}`\nhas been deleted.**"
        return t

    async def update_button(self, page: int):
        self.previous_button.disabled = page == 0
        self.next_button.disabled = page == len(self.pages) - 1
        self.select.options = self.create_options()

    def reset(self):
        self.select.placeholder = "Select an option"
        self.delete_button.disabled = True
        self.choices = question.create_question_list()
        self.select.options = self.create_options()
        self.pages = question.create_question_pages(self.title, self.url)
        for i in range(len(self.pages)):
            self.pages[i].set_thumbnail(self.image)
            self.pages[i].set_footer(text=f"Page {i + 1}/{len(self.pages)}")
        self.page_number = 0
        if question.questions_empty():
            self.select.disabled = True
        self.disable_button()
        if len(self.pages) > 1:
            self.next_button.disabled = False

    def create_options(self):
        return [nextcord.SelectOption(label=f"Question {i + self.page_number * 10 + 1}",
                                      value=str(i + self.page_number * 10))
                for i in range(len(self.choices[self.page_number]))]

    def disable_all_button(self):
        self.disable_button()
        self.select.disabled = True
        self.delete_button.disabled = True

    async def on_timeout(self) -> None:
        self.disable_all_button()
        og = await self.ctx.original_message()
        await og.edit(view=self, embed=self.pages[self.page_number])
