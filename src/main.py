from src.question import *


query = input('enter question: ')
answers = {}

for i in range(0, 3):
    answer = str(input("answer " + str(i) + ": "))
    answers[i] = answer

print(answers[get_answer(parse_query(query), answers)])
