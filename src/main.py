from src.question import *
from src.hebocr import *

query = input('enter question: ')
answers = {}

i = 0
while True:
    answer = str(input("add answer ( or enter to quit ): "))
    if answer is "":
        break
    answers[i] = answer
    i += 1

query = parse_query(query, answers)

print(query)
print("answer: " + answers[get_answer(query, answers, False)])
