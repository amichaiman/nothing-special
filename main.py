import src.imageprocess
from src.question import *

i = input("click enter or '4' for quick question: ")
quick = False

if i is '4':
    question, answers = src.imageprocess.get_question_and_answers_quick()
    quick = True
else:
    question, answers = src.imageprocess.get_question_and_answers()

question, answers = parse_input(question, answers)

print(question)
for i in range(0, answers.__len__()):
    print(answers[i])

#
# question = input('enter question: ')
#
# i = 0
# answers = {}
# while True:
#     answer = input('enter answer: ')
#     if answer == "":
#         break
#     answers[i] = answer
#     i += 1


print("answer: " + answers[get_answer(question, answers, quick)])











