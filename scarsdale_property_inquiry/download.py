import functools
import os

from picklecache import cache
import requests
from randua import generate as ua
from lxml.html import fromstring

from .fs import CACHE_DIRECTORY as C
from .navigate import house_postback, street_postback

def home():
    @cache(os.path.join(C))
    def f(key):
        return requests.get(p.url(), headers = p.headers(ua()))
    return f('home')

@cache(os.path.join(C))
def _post(section_name, _id, prev_response = None):
    data_func = {
        'house': house_postback,
        'street': street_postback,
    }[section_name]
    if prev_response == None:
        raise TypeError('prev_response must be defined.')

    html = fromstring(prev_response.text)
    data = data_func(html, _id)
    files = [(key, ('', str(value))) for key, value in data]
    return requests.post(p.url(), headers = p.headers(ua()),
                         files = files, cookies = prev_response.cookies)

street = functools.partial(_post, 'street')
house = functools.partial(_post, 'house')
