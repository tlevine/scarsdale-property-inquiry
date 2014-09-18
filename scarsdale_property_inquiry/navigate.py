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
