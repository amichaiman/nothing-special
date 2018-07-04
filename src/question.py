from src.webcrawl import *
import threading

lock = threading.Lock()
s = [0, 0, 0]


def add_occurence(i, html_text, search_term):
    reg = re.compile(search_term)
    with lock:
        s[i] += reg.findall(html_text).__len__()


def search_url(url, answers):
    try:
        html_text = get_html(url)
        html_text.encode('utf-8')
        for i, search_term in answers.items():
            t = threading.Thread(target=add_occurence, args=(i, html_text, search_term))
            t.daemon = True
            t.start()
    except:
        print("not good no no")


def get_answer(question, answers):
    url_list = google_search_result_websites(question)
    index_of_max = 0
    threads = []

    for url in url_list:
        thread = threading.Thread(target=search_url, args=(url, answers))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        # if threads.__len__() > 3:
        #     break

    for thread in threads:
        thread.join()

    for i in range(0, 3):
        if s[i] > s[index_of_max]:
            index_of_max = i

    return index_of_max


def parse_query(query):
    query = str(query)
    if query.find(u"השלם את המשפט") != -1:
        return query.split('\"')[1]
    return query
