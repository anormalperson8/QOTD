import nextcord

import question


class AddQuestion(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction, title: str = "Add a Question", channel=None):
        super().__init__(title)
        self.question_box = nextcord.ui.TextInput(label="Question", style=nextcord.TextInputStyle.paragraph,
                                                  min_length=1, required=True,
                                                  placeholder="Enter the question.")
        self.add_item(self.question_box)
        self.interaction = interaction
        self.channel = channel

    async def callback(self, interaction: nextcord.Interaction) -> None:
        question.add_to_filter(self.question_box.value.replace("\n", r"\n"))
        await interaction.send(f"Your question```\n{self.question_box.value}\n```has been added.\n"
                               "It will be put up for approval.", ephemeral=True)
        if self.channel is not None:
            await self.channel.send(f"Question```\n{self.question_box.value}\n```was submitted by "
                                    f"{interaction.user.global_name}")
