from urllib.parse import unquote
from lxml.html import fromstring

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

def compose_postback(html, event_target, event_argument, selected_option):
    inputs = (i.attrib for i in html.xpath('id("Form")//input'))
    data = {i['name']: i.get('value') for i in inputs}
    data['__EVENTTARGET'] = event_target
    data['__EVENTARGUMENT'] = event_argument
    selects = html.xpath('//select/@name')
    if len(selects) != 1:
        raise NotImplementedError('compose_postback expects exactly one select')
    data[selects[0]] = selected_option
    return data
