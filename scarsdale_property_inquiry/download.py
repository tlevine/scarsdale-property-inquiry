from urllib.parse import unquote
import functools
import os

from picklecache import cache
import requests
from randua import generate as ua
from lxml.html import fromstring

from .fs import CACHE_DIRECTORY as C
import scarsdale_property_inquiry.params as p

def parse_session(response):
    html = fromstring(response.text)

    publickeytoken = unquote(html.xpath('//script[contains(@src, "PublicKeyToken")]/@src')[0].split('PublicKeyToken=')[-1])
    viewstate = html.xpath('id("__VIEWSTATE")/@value')[0]
    eventvalidation = html.xpath('id("__EVENTVALIDATION")/@value')[0]
    return response.cookies, publickeytoken, viewstate, eventvalidation

def street_ids(html):
    return [str(value.strip()) for value in html.xpath('id("dnn_ctr1398_ViewHelloWorld_lstboxStreets")/option/@value')]

def house_ids(html):
    return [str(value.strip()) for value in html.xpath('id("dnn_ctr1398_ViewHelloWorld_lstboxAddresses")/option/@value')]

def home():
    @cache(os.path.join(C))
    def f(key):
        return requests.get(p.url(), headers = p.headers(ua()))
    return f('home')

def _post(section_name, data_func, _id, session = None):
    if session == None:
        raise TypeError('Session must be defined.')
    cookies, publickeytoken, viewstate, eventvalidation = session
    data = data_func(publickeytoken, viewstate, eventvalidation, _id)
    files = [(key, ('', str(value))) for key, value in data]
    return requests.post(p.url(), headers = p.headers(ua()), files = files, cookies = cookies)

def _street_house(street_house, session, _id):
    args = {
        'street': ('street', p.street_data),
        'house': ('house', p.house_data),
    }[street_house]
    directory = '~/.scarsdale-property-inquiry/' + args[0]
    f = cache(directory)(functools.partial(_post, *args))
    return f(_id, session = session)

street = functools.partial(_street_house, 'street')
house = functools.partial(_street_house, 'house')
