import src.imageprocess
from src.question import *

question, answers = src.imageprocess.get_question_and_answers()

print(question)
for i in answers:
    print(answers[i])

print("answer: " + answers[get_answer(question , answers, False)])
