from urllib.parse import unquote

from lxml.html import fromstring

import pi.cache

def parse_session(response):
    html = fromstring(response.text)

    publickeytoken = unquote(html.xpath('//script[contains(@src, "PublicKeyToken")]/@src')[0].split('PublicKeyToken=')[-1])
    viewstate = html.xpath('id("__VIEWSTATE")/@value')[0]
    eventvalidation = html.xpath('id("__EVENTVALIDATION")/@value')[0]
    return response.cookies, publickeytoken, viewstate, eventvalidation

def home():
    '() -> [street_id:str]'
    response = pi.cache.home()
    html = fromstring(response.text)

    session = parse_session(response)
    values = html.xpath('id("dnn_ctr1381_ViewPIRPS_lstboxStreets")/option/@value')
    street_ids = map(str, values)

    return session, street_ids

def street(session, street_id):
    'street_id -> [house_id:str]'
    response = pi.cache.street(session, street_id)
    html = fromstring(response.text)

    session = parse_session(response)
    values = html.xpath('id("dnn_ctr1381_ViewPIRPS_lstboxAddresses")/option/@value')
    house_ids = map(str, values)

    return session, house_ids

def house(session, house_id):
    'house_id -> house_data:dict'
    response = pi.cache.house(session, house_id)
    html = fromstring(response.text)
    property_number = html.xpath('id("dnn_ctr1381_ViewPIRPS_lblProperty")/text()')[0]
    return property_number, response.text
