import nextcord

from pageClass.InfoPages import InfoPages
import question


class QuestionPages(InfoPages):

    def __init__(self, *, timeout: int = 90, page_number: int = 0,
                 title: str = "", url: str = None, image=None,
                 ctx: nextcord.Interaction = None):
        self.title = title
        self.url = url
        self.image = image
        self.pages = question.create_question_pages(title=self.title, url=self.url)
        for i in range(len(self.pages)):
            self.pages[i].set_thumbnail(image)
            self.pages[i].set_footer(text=f"Page {i + 1}/{len(self.pages)}")
        super().__init__(timeout=timeout, pages=self.pages,
                         page_number=page_number, ctx=ctx)