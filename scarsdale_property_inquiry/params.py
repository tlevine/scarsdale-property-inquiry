def url():
    return 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'

def headers(user_agent):
    return {
        'User-Agent': user_agent,
        'Referer': url(),
        'Content-Encoding': 'gzip',
    }

def data(publickeytoken, viewstate, eventvalidation, eventtarget, value):
    return {
        'StylesheetManager_TSSM': '',
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=' + publickeytoken,
        '__EVENTTARGET': eventtarget,
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'dnn$SEARCH1$Search': 'SiteRadioButton',
        'dnn$SEARCH1$txtSearch': '',
        eventtarget: value,
        'dnn$dnnSEARCH$Search': 'SiteRadioButton',
        'dnn$dnnSEARCH$txtSearch': '',
        'ScrollTop': 228, # how far the page is scrolled
        '__dnnVariable': '{"__scdoff":"1"}',
    }

def house_data(publickeytoken, viewstate, eventvalidation, house_id):
    eventtarget = 'dnn$ctr1398$ViewHelloWorld$lstboxAddresses'
    result = data(publickeytoken, viewstate, eventvalidation, eventtarget, house_id)
    return result

def street_data(publickeytoken, viewstate, eventvalidation, street_id):
    eventtarget = 'dnn$ctr1398$ViewHelloWorld$lstboxStreets'
    result = data(publickeytoken, viewstate, eventvalidation, eventtarget, street_id)
    result['dnn$ctr1398$ViewHelloWorld$txtProperty'] = ''
    return result
