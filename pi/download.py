url = 'http://www.scarsdale.com/Home/Departments/InformationTechnology/PropertyInquiry.aspx'


def headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
        'Referer': url,
    }

def data():
    return {
        'StylesheetManager_TSSM': '',
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en:eb198dbd-2212-44f6-bb15-882bde414f00:ea597d4b:b25378d2',
        '__EVENTTARGET': 'dnn$ctr1381$ViewPIRPS$lstboxAddresses',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': __viewstate,
        '__EVENTVALIDATION': __eventvalidation,
        'dnn$SEARCH1$Search': 'SiteRadioButton',
        'dnn$SEARCH1$txtSearch': '',
       #'dnn$ctr1381$ViewPIRPS$lst...': '19.03.287',
        'dnn$ctr1381$ViewPIRPS$lstboxAddresses': '19.03.287',
        'dnn$dnnSEARCH$Search': 'SiteRadioButton',
        'dnn$dnnSEARCH$txtSearch': '',
        'ScrollTop': 228,
        '__dnnVariable': '{"__scdoff":"1"}',
    }
