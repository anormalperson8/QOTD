import os


path = os.path.dirname(os.path.abspath(__file__))


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

