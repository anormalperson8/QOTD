import nextcord

import question


class AddQuestion(nextcord.ui.Modal):
    def __init__(self, title: str = "Add a Question"):
        super().__init__(title)
        self.question_box = nextcord.ui.TextInput(label="Question", style=nextcord.TextInputStyle.paragraph,
                                                  min_length=1, max_length=4000,
                                                  required=True, placeholder="Enter the question.")
        self.add_item(self.question_box)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        question.add_to_filter(self.question_box.value.replace("\n", r"\n"))
        await interaction.send(f"Your question```\n{self.question_box.value}\n```has been added.\n"
                               "It will be put up for approval.", ephemeral=True)
