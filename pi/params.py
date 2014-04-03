def url():
    return 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'

def headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
        'Referer': url(),
    }

def data(publickeytoken, viewstate, eventvalidation, eventtarget, value):
    return {
        'StylesheetManager_TSSM': '',
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=' + publickeytoken,
      # '__EVENTTARGET': 'dnn$ctr1381$ViewPIRPS$lstboxAddresses',
        '__EVENTTARGET': eventtarget,
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'dnn$SEARCH1$Search': 'SiteRadioButton',
        'dnn$SEARCH1$txtSearch': '',
       #'dnn$ctr1381$ViewPIRPS$lst...': '19.03.287',
       #'dnn$ctr1381$ViewPIRPS$lstboxAddresses': '19.03.287',
        eventtarget: value,
        'dnn$dnnSEARCH$Search': 'SiteRadioButton',
        'dnn$dnnSEARCH$txtSearch': '',
        'ScrollTop': 228, # how far the page is scrolled
        '__dnnVariable': '{"__scdoff":"1"}',
    }
