from lxml.html import fromstring

import pi.cache

def home():
    '() -> [street_id:str]'
    response = pi.cache.home()
    html = fromstring(response.text)
    values = html.xpath('id("dnn_ctr1381_ViewPIRPS_lstboxStreets")/option/@value')
    return map(str, values)

def street():
    'street_id -> [house_id:str]'

def house():
    'house_id -> house_data:dict'
