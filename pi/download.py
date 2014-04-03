from lxml.html import fromstring

import pi.cache

def home():
    '() -> [street_id:str]'
    response = pi.cache.home()
    html = fromstring(response.text)

def street():
    'street_id -> [house_id:str]'

def house():
    'house_id -> house_data:dict'
