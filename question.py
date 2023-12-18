import os
import nextcord
import math
from itertools import zip_longest

import question
from info_command import random_colour

path = os.path.dirname(os.path.abspath(__file__))


# Possible TODO: Refactor txt files to json that holds question for each server


# Get list of questions
def get_questions():
    q = open(path + "/data/questions.txt", 'r')
    questions = q.read().split('\n')
    q.close()
    return questions


# Pop the first question out. Whether the file contains a question is NOT checked.
def pop_first_question():
    questions = get_questions()
    q = open(path + "/data/questions2.txt", 'w')
    q.write("\n".join(questions[1:]))
    q.close()
    os.remove(path + "/data/questions.txt")
    os.rename(path + "/data/questions2.txt", path + "/data/questions.txt")
    return questions[0]


# Get questions to be filtered
def get_filters():
    f = open(path + "/data/filter.txt", 'r')
    questions = f.read().split('\n')
    f.close()
    return questions


# Accept or deny a question
def filter_question(index: int, status: bool):
    questions = get_filters()
    new_q = get_questions()

    # Update questions
    if status:
        new_q.append(questions.pop(index))
        q = open(path + "/data/questions2.txt", 'w')
        q.write("\n".join(new_q))
        q.close()
        os.remove(path + "/data/questions.txt")
        os.rename(path + "/data/questions2.txt", path + "/data/questions.txt")

    # Update filters
    f = open(path + "/data/filter2.txt", 'w')
    if status:
        f.write("\n".join(questions))
    else:
        f.write("\n".join(questions[:index] + questions[index + 1:]))
    f.close()
    os.remove(path + "/data/filter.txt")
    os.rename(path + "/data/filter2.txt", path + "/data/filter.txt")


def create_approve_list():
    return [list(filter(lambda i: i is not None, que)) for que in list(zip_longest(*[iter(get_filters())] * 10))]


def create_approve_pages(title: str, url: str):
    # TODO: Create pages for approval (should be server-specific?)

    it = create_approve_list()

    text = [("Approve/Reject questions by selecting below and click the corresponding button!\n"
             "Questions:\n" +
             "\n".join(
                [f"{(10 * i + j + 1):2d}: {it[i][j]}" for j in range(len(it[i]))]
             ) +
             "\n") for i in range(len(it))]

    return [nextcord.Embed(title=title,
                           description=f"```\n{t}```",
                           colour=random_colour(), url=url) for t in text]


if __name__ == "__main__":
    print(create_approve_pages("haha", "")[0].description)
