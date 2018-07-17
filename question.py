from src.webcrawl import *
import threading
import time
import pyautogui

sum_lock = threading.Lock()
index_of_answer_lock = threading.Lock()

s = []
found = False
index_of_answer = 0
opposite = False
unique = False
threads = []
answer_clicked = False
quick = False
snooze_count = 0


def print_answers(answers):
    global opposite
    global answer_clicked
    global index_of_answer

    if not answer_clicked:
        answer_clicked = True
        simulate_click(answers)
    try:
        print('%s : %.2f' % (answers[index_of_answer], s[index_of_answer] / sum(s) * 100) + '%')
        for i in range(0, answers.__len__()):
            if i is not index_of_answer:
                print('%s %.2f' % (answers[i], s[i] / sum(s) * 100) + '%')
    except:
        print("couldn't compute an answer")
        return


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
                with index_of_answer_lock:
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
                with index_of_answer_lock:
                    index_of_answer = i
                print_answers(answers)
                found = True
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


def simulate_click(answers):
    global quick
    global index_of_answer

    if sum(s) is 0:
        print("guessing")
        index_of_answer = 1

    if index_of_answer is 0:
        for i in range(0, answers.__len__()):
            if opposite:
                if s[i] < s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i
            else:
                if s[i] > s[index_of_answer]:
                    with index_of_answer_lock:
                        index_of_answer = i
    if not quick:
        if index_of_answer is 0:
            pyautogui.click((110 + 350) / 2, (557 + 595) / 2)
        elif index_of_answer is 1:
            pyautogui.click((110 + 350) / 2, (608 + 650) / 2)
        elif index_of_answer is 2:
            pyautogui.click((110 + 350) / 2, (660 + 700) / 2)
    else:
        if index_of_answer is 0:
            pyautogui.click((110 + 350) / 2, (505 + 545) / 2)
        elif index_of_answer is 1:
            pyautogui.click((110 + 350) / 2, (560 + 595) / 2)
        elif index_of_answer is 2:
            pyautogui.click((110 + 350) / 2, (610 + 645) / 2)
        elif index_of_answer is 3:
            pyautogui.click((110 + 350) / 2, (665 + 700) / 2)


def print_soon(answers, length):
    global index_of_answer
    global answer_clicked
    global snooze_count

    time.sleep(length)

    if sum(s) > 0:
        if not found:
            print("***********************************************")
            print("************       estimate        ************")
            print("***********************************************")
            print_answers(answers)
            print("***********************************************")
    else:
        snooze_count += 1
        if snooze_count is 2:
            simulate_click(answers)
        print_soon(answers, 2)


def get_answer(question, answers, fast):
    global s
    global index_of_answer
    global opposite
    global answer_clicked
    global quick

    s = [0 for i in range(0, answers.__len__())]

    quick = fast
    weight = 10
    url_list = google_search_result_websites(question)

    add_google_page_matches(question, answers, weight)

    if quick:
        simulate_click(answers)
        for thread in threads:
            thread.join()
        return index_of_answer

    timer = threading.Thread(target=print_soon, args=(answers, 2.5))
    timer.daemon = True
    timer.start()

    for url in url_list:
        thread = threading.Thread(target=search_url, args=(url, answers, weight))
        thread.daemon = True

        if found:
            for thread in threads:
                thread.join()
            return index_of_answer

        threads.append(thread)
        thread.start()
        weight = weight * 0.7

    for thread in threads:
        thread.join()

    if not found:
        print_answers(answers)

    return index_of_answer


def concatenate_answers(answers):
    query = ""
    for i in range(0, answers.__len__()):
        query += answers[i] + " "
    return query


def remove_redundant_words(query):
    query = " " + query + " "
    for word in [u'מה', u'אותי', u'איזה', u'מי', u'אם', u'הייתי', u'הגעתי', u'כנראה', u'עליהם', u'איזו', u'אילו', u'מהו'
        , u'איך', u'קוראים', u'היכן', u'סביר', u'להניח', u'היה', u'את', u'ניתן', u'אני', u'של']:
        reg = re.compile(r'\b.?' + word + r'\b')
        for match in reg.findall(query):
            # print(match)
            loc = query.find(match)
            if loc is not -1:
                query = query[:loc] + query[loc + match.__len__():]

    reg = re.compile('[,.?]')
    for match in reg.findall(query):
        query = query.replace(match, '')

    reg = re.compile('\s\s+|\n')
    extra_chars = ['\s\s+', '\n', ',', '.', '/?']
    for extra_char in extra_chars:
        query = query.replace(extra_char, ' ')

    return query


def remove_word(query, to_remove):
    return query.replace(to_remove, ' ')


def parse_input(query, answers):
    global opposite
    global unique
    concatenated_answers = concatenate_answers(answers)

    # parse answers
    reg_count = [0, 0]
    for i in range(0, answers.__len__()):
        answers[i] = answers[i].replace(u"'", u"[י']")
        answers[i] = answers[i].replace(u"נ", u"[נב]")
        answers[i] = answers[i].replace(u"ח", u"[חת]")
        answers[i] = answers[i].replace(u"ך", u"[ךר]")
        # get rid of [,.|]
        reg = re.compile(u'[,.|”]')
        for match in reg.findall(answers[i]):
            answers[i] = answers[i].replace(match, u"")

        # if all answers start with ב or all start with ל, get rid of them
        try:
            if answers[i][0] == u'ב':
                reg_count[0] += 1
            elif answers[i][0] == u'ל':
                reg_count[1] += 1
        except:
            pass
    if reg_count[0] == answers.__len__() or reg_count[1] == answers.__len__():
        for i in range(0, answers.__len__()):
            answers[i] = answers[i][1:]

    # parse question
    reg = re.compile(u'[,.|”־:]')
    for match in reg.findall(query):
        query = query.replace(match, '')
    if query.find(u'יוצא דופן') != -1:
        unique = True
        opposite = True
        return concatenated_answers, answers

    if query.find(u'הבאים') != -1 or query.find(u'הבאות') != -1:
        opposites = [u'אין', u'לא', u'איננו']
        for o in opposites:
            reg = re.compile(r'\b.?' + o + r'\b')
            for match in reg.findall(query):
                loc = query.find(match)
                query = query[loc + o.__len__() + 1:]
                opposite = True
                unique = True

        query = query.replace(u'הבאים', '')
        query = query.replace(u'הבאות', '')

        return remove_redundant_words(query) + " " + concatenated_answers, answers

    try:
        query = query.replace("'", u"י")
        query = query.replace('\n', ' ')
        return re.split('"', query)[1], answers
    except:
        return remove_redundant_words(query), answers
