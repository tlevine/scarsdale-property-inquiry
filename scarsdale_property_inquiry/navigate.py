from functools import partial
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

def url():
    return 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'

def headers(user_agent):
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'User-Agent': user_agent,
        'Referer': url(),
        'Content-Encoding': 'gzip',
    }

def _compose_postback(event_target, event_argument, html, selected_option):
    selects = html.xpath('//select/@name')
    if len(selects) != 1:
        raise NotImplementedError('compose_postback expects exactly one select')
    data = {selects[0]: selected_option}

    inputs = (i.attrib for i in html.xpath('id("Form")//input'))
    data.update({i['name']: i.get('value') for i in inputs})
    data.update({
        '__EVENTTARGET': event_target,
        '__EVENTARGUMENT': event_argument,
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=' + publickeytoken,
    })
    return data

house_postback = partial(compose_postback,
    'dnn$ctr1398$ViewHelloWorld$lstboxAddresses', '')
street_postback = partial(compose_postback,
    'dnn$ctr1398$ViewHelloWorld$lstboxStreets', '')
