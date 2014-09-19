from functools import partial
from urllib.parse import unquote

def street_ids(html):
    return [str(value.strip()) for value in html.xpath('id("dnn_ctr1398_ViewHelloWorld_lstboxStreets")/option/@value')]

def house_ids(html):
    return [str(value.strip()) for value in html.xpath('id("dnn_ctr1398_ViewHelloWorld_lstboxAddresses")/option/@value')]

def url():
    return 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'

def headers(user_agent, cookies):
    cookie = '; '.join(key + '=' + value for key, value in cookies.items())
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Content-Encoding': 'gzip',
        'Host': 'www.scarsdale.com',
        'Origin': 'http://www.scarsdale.com',
        'Referer': url(),
        'User-Agent': user_agent,
    }

def _compose_postback(event_target, event_argument, html, value):
    data = {}

    inputs = (i.attrib for i in html.xpath('id("Form")//input'))
    data.update({i['name']: i.get('value') for i in inputs})

    publickeytoken = unquote(html.xpath('//script[contains(@src, "PublicKeyToken")]/@src')[0].split('PublicKeyToken=')[-1])

    data.update({
        '__EVENTTARGET': event_target,
        '__EVENTARGUMENT': event_argument,
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=' + publickeytoken,
    })

    data['ScrollTop'] = '228'
    data[event_target] = value
    return data

house_postback = partial(_compose_postback,
    'dnn$ctr1398$ViewHelloWorld$txtProperty', '')
street_postback = partial(_compose_postback,
    'dnn$ctr1398$ViewHelloWorld$lstboxStreets', '')
