import functools
import datetime
import os

from picklecache import cache
import requests
from randua import generate as ua
from lxml.html import fromstring

from .fs import CACHE_DIRECTORY as C
from .navigate import house_postback, street_postback, url, headers

def home():
    @cache(os.path.join(C, 'home'))
    def f(key):
        return requests.get(url(), headers = headers(ua(), {}),
                            allow_redirects = False)
    return f(datetime.date.today().isoformat())

def _post_args(section_name, _id, prev_response, user_agent = ua()):
    data_func = {
        'house': house_postback,
        'street': street_postback,
    }[section_name]

    html = fromstring(prev_response.text)
    data = data_func(html, _id)
    files = [(key, ('', '' if value == None else str(value))) \
             for key, value in data.items()]
    args = url(),
    kwargs = {
        'headers': headers(user_agent, prev_response.cookies),
        'files': files,
    }
    return args, kwargs

@cache(os.path.join(C))
def _post(section_name, _id, prev_response = None):
    if prev_response == None:
        raise TypeError('prev_response must be defined.')
    args, kwargs = _post_args(section_name, _id, prev_response)
    kwargs['allow_redirects'] = False
    return requests.post(*args, **kwargs)

street = functools.partial(_post, 'street')
house = functools.partial(_post, 'house')
