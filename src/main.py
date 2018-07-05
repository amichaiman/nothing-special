from src.question import *
from src.hebocr import *

query = input('enter question: ')
answers = {}

for i in range(0, 3):
    answer = str(input("answer " + str(i) + ": "))
    answers[i] = answer

query = parse_query(query, answers)
print(query)
print("answer: " + answers[get_answer(query, answers, False)])
