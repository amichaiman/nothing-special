from src.webcrawl import *


def get_answer(question, answers):
    url_list = google_search_result_websites(question)
    sum = [0, 0, 0]
    index_of_max = 0

    for url in url_list:
        try:
            print(url)
            html_text = get_html_text(url)
            for i, search_term in answers.items():
                sum[i] += get_occurrence_number(html_text, search_term)
                if sum[i] > sum[index_of_max]:
                    index_of_max = i

                print(sum[index_of_max])
                print(sum[i])
                # for j in range(0, answers.__len__()):
                #     if i != j and sum[i] - sum[j] > 10:
                #         return i
        except:
            print("not good no no")

    return index_of_max


def parse_query(query):
    query = str(query)
    if query.find(u"השלם את המשפט") != -1:
        return query.split('\"')[1]
    return query
