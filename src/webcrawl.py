import re
import urllib.request
from lxml import html
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_occurrence_number(html_text, pattern):
    reg = re.compile(pattern)
    return reg.findall(html_text).__len__()


def get_websites(url):
    html_text = get_html_text(url)
    print(html_text)
    regex = re.compile(r'http[^"]*')
    url_set = set()
    for link in regex.findall(html_text):
        print(link[6:])
        url_set.add(link[9:])
    return url_set


def get_html_text(url):
    request = requests.get(url)
    return request.content.__str__()


def google_search_result_websites(search_request):
    return get_websites(google_search_url(search_request))


def google_search_url(search_query):
    url = 'https://www.google.com/search?q='
    url += quote(search_query)
    return url


def get_header():
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 'r'Safari/537.36 '}
    return headers
