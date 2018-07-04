from typing import List

from src.webcrawl import *
import threading

sum_lock = threading.Lock()
index_of_answer_lock = threading.Lock()

s = [0, 0, 0]
found = False
index_of_answer = 0
opposite = False
unique = False
threads = []


def add_occurrence(i, html_text, search_term, answers):
    global found
    global sum_lock
    global index_of_answer
    global opposite

    if found:
        return
    if unique:
        reg = re.compile(u'חסר:*.{0}*.'.format(search_term))
        if reg.findall(html_text).__len__() > 0:
            print(answers[i])
            with sum_lock:
                found = True
                index_of_answer = i

    reg = re.compile(u'[ (למהו.,/"]?' + search_term + u'[ -)!?.",/]')

    if found:
        return

    with sum_lock:
        s[i] += reg.findall(html_text).__len__()

    if opposite:
        less_count = 0
        for j in range(0, answers.__len__()):
            if i != j and s[j] - s[i] > 5:
                less_count = less_count + 1
        if less_count == answers.__len__() - 1:
            with sum_lock:
                print(answers[i])
                found = True
                index_of_answer = i
                return

    for j in range(0, answers.__len__()):
        if not opposite and s[i] - s[j] > 14:
            if found:
                return
            with sum_lock:
                found = True
            with index_of_answer_lock:
                index_of_answer = i
                print(answers[i])


def search_url(url, answers):
    try:
        # print(url)
        html_text = get_html(url)
        html_text.encode('utf-8')
        for i, search_term in answers.items():
            t = threading.Thread(target=add_occurrence, args=(i, html_text, search_term, answers))
            t.daemon = True

            if found:
                return

            t.start()
    except:
        pass


def add_google_page_matches(question, answers):
    google_url = google_search_url(question)
    # print(google_url)
    google_html = get_html(google_url)
    for i in range(0, answers.__len__()):
        thread = threading.Thread(target=add_occurrence, args=(i, google_html, answers[i], answers))
        thread.daemon = True
        thread.start()
        threads.append(thread)


def get_answer(question, answers, quick):
    global s
    global index_of_answer
    global opposite

    parse_answer(answers)

    url_list = google_search_result_websites(question)

    google_url = google_search_url(question)
    # print(google_url)
    google_html = get_html(google_url)

    add_google_page_matches(question, answers)

    if not quick and not unique:
        for url in url_list:
            thread = threading.Thread(target=search_url, args=(url, answers))
            thread.daemon = True
            threads.append(thread)
            if found:
                return index_of_answer

            thread.start()

    for thread in threads:
        thread.join()

    if not found:
        for i in range(0, 3):
            print(answers[i], s[i])
            if opposite:
                if s[i] < s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i
            else:
                if s[i] > s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i

    return index_of_answer


def concatinate_answers(answers):
    query = ""
    for i in range(0, answers.__len__()):
        query += answers[i] + " "
    return query

def parse_query(query, answers):
    global opposite
    global unique

    query = str(query)

    if query.find(u'יוצא דופן') != -1:
        query = concatinate_answers(answers)
        unique = True
        opposite = True
        return query
    if query.find(u'מי מהבאים') != -1:
        query = concatinate_answers(answers)
        unique = True

    if query.find(u'לא') != -1:
        query.replace(u'לא', '')
        opposite = True
    try:
        return query.split('\"')[1]
    except:
        return query


def parse_answer(answers):
    reg_count = [0, 0]
    for i in range(0, answers.__len__()):
        if answers[i][0] == u'ב':
            reg_count[0] += 1
        elif answers[i][0] == u'ל':
            reg_count[1] += 1

    if reg_count[0] == answers.__len__() or reg_count[1] == answers.__len__():
        for i in range(0, answers.__len__()):
            answers[i] = answers[i][1:]
