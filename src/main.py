import src.imageprocess
from src.question import *

# question, answers = src.imageprocess.get_question_and_answers()


# question, answers = parse_input(question, answers)
# print(question)
# for i in answers:
#     print(answers[i])


question = input('enter question')

i = 0
answers = {}
while True:
    answer = input('enter answer')
    if answer == "":
        break
    answers[i] = answer
    i += 1

print("answer: " + answers[get_answer(question, answers, False)])
