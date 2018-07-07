from src.webcrawl import *
import threading
import time

sum_lock = threading.Lock()
index_of_answer_lock = threading.Lock()

s = []
found = False
index_of_answer = 0
opposite = False
unique = False
threads = []


def print_answers(answers):
    global opposite

    try:
        print('%s : %.2f' % (answers[index_of_answer], s[index_of_answer] / sum(s) * 100) + '%')
        for i in range(0, answers.__len__()):
            if i is not index_of_answer:
                print('%s %.2f' % (answers[i], s[i] / sum(s) * 100) + '%')
    except:
        print("couldn't compute an answer")
        print_soon(answers, 2)


def add_occurrence(i, html_text, search_term, answers, weight):
    global found
    global sum_lock
    global index_of_answer
    global opposite

    if found:
        return
    if unique:
        reg = re.compile(u'חסר:*.{0}*.'.format(search_term))
        if reg.findall(html_text).__len__() > 0:
            print_answers(answers)
            with sum_lock:
                found = True
                index_of_answer = i

    reg = re.compile(u'[ (למהו.,/"]?' + search_term + u'[ -)!?.",/]')

    if found:
        return

    with sum_lock:
        s[i] += reg.findall(html_text).__len__() * weight

    if opposite:
        less_count = 0
        for j in range(0, answers.__len__()):
            if i != j and s[j] - s[i] > 70:
                less_count = less_count + 1
        if less_count == answers.__len__() - 1:
            with sum_lock:
                print_answers(answers)
                found = True
                index_of_answer = i
                return

    for j in range(0, answers.__len__()):
        if not opposite and s[i] - s[j] > 150:
            if found:
                return
            with sum_lock:
                found = True
            with index_of_answer_lock:
                index_of_answer = i
                print_answers(answers)


def search_url(url, answers, weight):
    try:
        # print(url)
        html_text = get_html(url)
        html_text.encode('utf-8')
        for i, search_term in answers.items():
            t = threading.Thread(target=add_occurrence, args=(i, html_text, search_term, answers, weight))
            t.daemon = True

            if found:
                return

            t.start()
    except:
        pass


def add_google_page_matches(question, answers, weight):
    google_url = google_search_url(question)
    print(google_url)
    google_html = get_html(google_url)
    for i in range(0, answers.__len__()):
        thread = threading.Thread(target=add_occurrence, args=(i, google_html, answers[i], answers, weight))
        thread.daemon = True
        thread.start()
        threads.append(thread)


def print_soon(answers, length):
    time.sleep(length)

    if not found:
        print("***********************************************")
        print("************       estimate        ************")
        print("***********************************************")
        print_answers(answers)
        print("***********************************************")


def get_answer(question, answers, quick):
    global s
    global index_of_answer
    global opposite

    s = [0 for i in answers]

    timer = threading.Thread(target=print_soon, args=(answers, 2))
    timer.daemon = True
    timer.start()

    weight = 10
    url_list = google_search_result_websites(question)

    add_google_page_matches(question, answers, weight)

    if not quick and not unique:
        for url in url_list:
            thread = threading.Thread(target=search_url, args=(url, answers, weight))
            thread.daemon = True
            threads.append(thread)
            if found:
                return index_of_answer

            thread.start()
            weight = weight * 0.7
    for thread in threads:
        thread.join()

    if not found:
        for i in range(0, answers.__len__()):
            if opposite:
                if s[i] < s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i
            else:
                if s[i] > s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i

    if not found:
        print_answers(answers)
    return index_of_answer


def concatinate_answers(answers):
    query = ""
    for i in range(0, answers.__len__()):
        query += answers[i] + " "
    return query


def remove_redundant_words(query):
    query = " " + query + " "
    for word in [u'מה', u'איזה', u'מי', u'אם', u'הייתי', u'הגעתי', u'כנראה', u'עליהם', u'איזו', u'אילו', u'מהו'
        , u'איך', u'קוראים', u'היכן', u'סביר', u'להניח', u'אותי', u'היה', u'את', u'ניתן', u'אני', u'של']:
        reg = re.compile(u'[ ].?' + word + '[ ]')
        for match in reg.findall(query):
            # print(match)
            if query.find(word):
                if match[-1] == ' ':
                    query = remove_word(query, match[1:-1])
                else:
                    query = remove_word(query, match[1:-1])
    return query


def remove_word(query, to_remove):
    return query.replace(to_remove, '')


def parse_input(query, answers):
    global opposite
    global unique

    # parse answers
    reg_count = [0, 0]

    for i in range(0, answers.__len__()):
        # answers[i] = answers[i].replace("'", u"י")
        if answers[i][0] == u'ב':
            reg_count[0] += 1
        elif answers[i][0] == u'ל':
            reg_count[1] += 1

    if reg_count[0] == answers.__len__() or reg_count[1] == answers.__len__():
        for i in range(0, answers.__len__()):
            answers[i] = answers[i][1:]

    # parse question
    if query.find(u'יוצא דופן') != -1:
        query = concatinate_answers(answers)
        unique = True
        opposite = True
        return query

    if query.find(u'מהבאים') != -1 or query.find(u'מהבאות') != -1:
        if query.find(u'לא') != -1:
            query = query[query.find(u'לא ') + 3:]
            opposite = True
            unique = True
            return query + " " + concatinate_answers(answers), answers

        query = query[query.find(u'מהבא') + 6:]
        return query
    loc = query.find(u'לא ')
    if loc != -1:
        query = query[:loc] + query[loc + 3:]
        opposite = True
    try:
        return query.split('\"')[1], answers
    except:
        return remove_redundant_words(query), answers
