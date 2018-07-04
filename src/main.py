from src.question import *

query = input('enter question: ')
answers = {}

for i in range(0, 3):
    answer = str(input("answer " + str(i) + ": "))
    answers[i] = answer

query = parse_query(query, answers)
print("answer: " + answers[get_answer(query, answers, False)])
